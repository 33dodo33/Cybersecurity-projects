#Tool to GeoTrack all sources of IP 
#The PCAP file name need to be adjusted in the code and added to the file location
#An example of render:



import dpkt
import socket
import pygeoip

gi = pygeoip.GeoIP('GeoLiteCity.dat')
gi.country_name_by_addr('14.139.61.12')

def retKML(dstip, srcip):
     dst = gi.record_by_name(dstip)
     src = gi.record_by_name('x.xxx.xxx.xxx') #Inpput your own IP address here 
     try:
          dstlongitude = dst['longitude']
          dstlatitude = dst['latitude']
          srclongitude = src['longitude']
          srclatitude = src['latitude']
          kml = (
               '<Placemark>\n'
               '<name>%s</name>\n'
               '<extrude>1</extrude>\n'
               '<tesellate>1</tesellate>\n'
               '<styleUrl>#transBluePoly</styleUrl>\n'
               '<LineString>\n'
               '<coordinates>%6f, \n%6f, %6f</coordinates>\n'
               '</LineString>\n'
               '</Placemark>'
               
        )%(dstip, dstlongitude, dstlatitude, srclongitude, srclatitude)
          return kml
     execpt:
     return ''




def plotIPs(pcap):
    klmPts = '' 
    for (ts, buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            KML = retKML(dst, src)
            kmlPts - kmlPts +  KML
        except:
            pass
        return kmlPts      



def main():
    f = open('wire.pcap', 'rb')
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<7xml version="1.0" encoding="UTF-8"?> \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'\
    '<Style id=transBluePoly">' \
            '<LineStyle>' \
            '<width>1.5</width>' \
            '<color>501400E6</color>' \
            '</LineStyle>' \
            '</Style>' \
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print(kmldoc)

if __name__ == '__main__':
        main()
