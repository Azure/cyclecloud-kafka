import unittest
import subprocess
import time
import jetpack.config


def _kafka_ready():
    '''The function actually asks zookeeper if all of the kafka brokers are registered'''
    p = subprocess.Popen(['/opt/kafka/bin/zookeeper-shell.sh', 'localhost:2181'],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate('ls /brokers/ids')
    return (p, stdout, stderr)


def zk_ready():
    p = subprocess.Popen(['systemctl', 'status', 'zookeeper'])
    p.communicate()
    return p.returncode == 0


def kafka_service_ready():
    p = subprocess.Popen(['systemctl', 'status', 'kafka'])
    p.communicate()
    return p.returncode == 0


def kafka_ready():
    '''Calls zkCli.sh get / until it responds w/out a failure'''
    timeout = (60 * 5)
    ensemble_size = jetpack.config.get('zookeeper.ensemble_size')

    # first, check if zookeeper is running
    is_zk_ready = zk_ready()
    if not is_zk_ready:
        return False, 'Zookeeper service not running', ''
    
    # 5 minutes from now
    deadline = timeout + time.time()
    success = False
    stdout = ''
    stderr = ''
    while time.time() < deadline:
        # the kafka service cannot start until
        # zookeeper has reached quorum, which can take a while
        if not kafka_service_ready():
            stdout = 'Kafka service not running'
            continue
        
        p, stdout, stderr = _kafka_ready()
        if p.returncode == 0:
            last_line = stdout.strip().split('\n')[-1]
            if not last_line.startswith('['):
                pass
            else:
                # never, ever use eval in production code
                members = eval(last_line)
                if len(members) == ensemble_size:
                    success = True
                    break

    return success, stdout, stderr


class TestKafkaBroker(unittest.TestCase):

    def setUp(self):
        self.hostname = subprocess.check_output('hostname').strip()
        self.topic = 'test_%s' % self.hostname

    def tearDown(self):
        subprocess.check_call(['/opt/kafka/bin/kafka-topics.sh', '--delete', '--zookeeper',
                               'localhost:2181', '--topic', self.topic])
        
    def test_create_topic(self):
        ready, stdout, stderr = kafka_ready()
        self.assertTrue(ready,
                        msg="Kafka ensemble not ready after 5 minutes\nStdout: %s\nStderr: %s"
                        % (stdout, stderr))

        subprocess.check_call(['/opt/kafka/bin/kafka-topics.sh', '--create', '--zookeeper',
                               'localhost:2181', '--replication-factor', '1', '--partitions', '1',
                               '--topic', self.topic])

        output = subprocess.check_output(['/opt/kafka/bin/kafka-topics.sh', '--list',
                                          '--zookeeper', 'localhost:2181'])
        
        self.assertTrue(self.topic in output, msg="Topic %s not created" % self.topic)
