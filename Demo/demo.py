from jenkinsapi.jenkins import Jenkins


def get_server_instance():
    jenkins_url = 'http://lixin:112383f35d26a61c03c51b132e330438f2@192.168.50.41:8088/'
    server = Jenkins(jenkins_url)
    return server


if __name__ == '__main__':
    print
    get_server_instance().version()
