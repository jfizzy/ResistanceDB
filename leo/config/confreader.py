import re

def main():
    with open('config.cfg') as f:
        lines = f.readlines()
    if lines:
        for line in lines:
            line.strip()
            if '#' in line:
                line = line.split('#')[0].strip()
            if re.match('^$', line):
                # empty line
                print('empty line: ['+line.split('\n')[0]+']')
                pass
            elif re.match('^COMPOUNDS=[a-zA-Z09_]+.[a-z]+$', line):    
                # compounds filename line
                print('compounds line: ['+line.split('\n')[0]+']')
                pass
            elif re.match('^MINMZ=[0-9]+(.[0-9]+)?e[0-9]+$', line):
                # Minimum intensity
                print('min intensity line: ['+line.split('\n')[0]+']')
                pass
            elif re.match('^MAXRTDIFF=[0-9]+.[0-9]+$', line):
                # maximum Retention time differential
                print('rt differential line: ['+line.split('\n')[0]+']')
                pass
            elif re.match('^MZDIFF=((0.[0-9]+)|0|1)$', line):
                # intensity differential %
                print('intensity differential line: ['+line.split('\n')[0]+']')
                pass
            else:
                #invalid line
                print('invalid line: ['+line.split('\n')[0]+']')
                pass

if __name__ == "__main__":
    main()
