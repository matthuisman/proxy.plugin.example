import sys
import xbmcgui, xbmcplugin

example_url = 'https://bitmovin-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8'

handle = int(sys.argv[1])

play_url = 'http://127.0.0.1:9999/' + example_url
li = xbmcgui.ListItem('Play!')
li.setProperty('IsPlayable', 'true')
li.setPath(play_url)

xbmcplugin.addDirectoryItem(handle, play_url, li, False)
xbmcplugin.endOfDirectory(handle, succeeded=True)
