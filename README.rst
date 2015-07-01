=======
mayloop
=======

An asynchronous i/o library.


Features
========
* Asynchronous i/o loop to run socket servers.
* Telnet interface to control the loop, print the stats, etc.


Usage
=====
The following code sample creates a simple protocol that just sends back the message it receives and then starts a server that will use the protocol::

        class Talkback(FixedLengthMessage):
                def messageReceived(self, message):
                        self.sendMessage(message)

        config = Config()
        config.add_service('', 8080, Factory.forProtocol(Talkback))

        server = MainLoop(config)
        server.start()



Download
========
* PyPI: http://pypi.python.org/pypi/mayloop
* Source: https://github.com/amol9/mayloop

