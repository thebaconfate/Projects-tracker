import src.workhours as wh
import src.workhoursdecoder as dec
import src.workhoursencoder as enc

testing = True
if testing:
    filename = 'files/test_workhours.json'
else: 
    filename = 'files/workhours.json'
    
def main():
    workhours = wh.WorkHours(filename=filename, encoder=enc.WorkhoursEncoder, decoder=dec.WorkhoursDecoder().default)
    workhours.load_workhours()
    workhours.run()
    print('Ended program.')

if __name__ == "__main__":
    main()
