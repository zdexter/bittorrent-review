from client import BittorrentClient
import msg
import strategy

def main():
    client = BittorrentClient()
    torrent = client.add_torrent('flagfromserver.torrent')
    #torrent = client.add_torrent('test.torrent')
    torrent.tracker_update()

    print 'file length:', torrent.length

    print 'got these peers from tracker:', torrent.tracker_peer_addresses
    external_ip = torrent.get_external_addr()
    print 'removing', (external_ip, client.port), 'if it appears because it looks like it\'s us'
    addresses = filter(lambda ipport:(external_ip, client.port) != ipport, torrent.tracker_peer_addresses)
    print 'so just using', addresses

    if not addresses:
        print 'no one else on tracker!'
        return

    print addresses
    address = [x for x in addresses if x[0].startswith('9')][0]
    peer = torrent.add_peer(*address)
    peer.connect()
    #peer = torrent.add_peer('', 8001)
    peer.send_msg(msg.interested())
    peer.strategy = strategy.keep_asking_strategy
    peer.run_strategy()
    while True:
        r = client.reactor.poll(1)
        if r is None:
            return

if __name__ == '__main__':
    main()
