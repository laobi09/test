import sys, os, time, random, wave, math, pyaudio, argparse
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from collections import deque

# 是否通过图表展示算法的执行过程
gShowPlot = False

# 小调五声音阶
pmNotes = {'C4':262, 'Eb':311, 'F':349, 'G':391, 'Bb':466}

CHUNK = 1024

fig, ax = plt.subplots(1)
line, = ax.plot([],[])


def writeWave(fname, data):
    """将数据写入data文件"""
    file = wave.open(fname, 'wb')
    nChannels = 1
    sampleWidth = 2
    frameRate = 44100
    nFrames = 44100
    file.setparams((nChannels, sampleWidth, frameRate, nFrames,
                    'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close()


def generateNote(freq):
    """使用KS算法生成音符"""
    sRate = 44100
    nSamples = sRate * 1
    N = int(sRate/freq)

    if gShowPlot:
        ax.set_xlim([0,N])
        ax.set_ylim([-1.0,1.0])
        line.set_xdata(np.arange(0,N))

    # 初始化环形缓冲区
    buf = deque([random.random()-0.5 for i in range(N)],maxlen=N)
    # 初始化样本缓冲区
    samples = np.array([0]*nSamples, 'float32')

    # Karplus-Strong算法, 模拟吉他音色
    for i in range(nSamples):
        samples[i] = buf[0]
        avg = 0.995*0.5*(buf[0]+buf[1])
        buf.append(avg)
        if gShowPlot:
            if i % 1000 ==0:
                line.set_ydata(buf)
                fig.canvas.draw()
                fig.canvas.flush_events()
    samples = np.array(samples*32767, 'int16')
    return samples.tobytes()



class NotePlayer:
    def __init__(self):
        # 初始化pyaudio
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                output=True)
        self.notes=[]
    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def add(self, fileName):
        self.notes.append(fileName)

    def play(self, fileName):
        try:
            print("playing "+fileName)
            wf = wave.open(fileName, 'rb')
            data = wf.readframes(CHUNK)
            while data != b'':
                self.stream.write(data)
                data = wf.readframes(CHUNK)
            wf.close()
        except BaseException as err:
            print(f"Exception! {err=}, {type(err)=}.\Exiting.")
            exit(0)
    
    def playRandom(self):
        index = random.randint(0,len(self.notes)-1)
        note = self.notes[index]
        self.play(note)

def main():
    parser = argparse.ArgumentParser(description="Generating sounds with Karplus-Strong Algorithm")
    parser.add_argument('--display', action='store_true', required=False)
    parser.add_argument('--play', action = 'store_true', required=False)
    args = parser.parse_args()

    if args.display:
        gShowPlot = True
        plt.show(block=False)

    nplayer = NotePlayer()
    print('creating notes...')

    for name, freq in list(pmNotes.items()):
        filename = name + '.wav'
        if not os.path.exists(filename) or args.display:
            data = generateNote(freq)
            print('creating ' + filename + '...')
            writeWave(filename, data)
        else:
            print('filename already created. skipping...')

        # 将文件名添加到播放器中
        nplayer.add(name + '.wav')

        # 如果设置了标志display，就播放WAV文件
        if args.display:
            nplayer.play(name+'.wav')
            time.sleep(0.5)

        if args.play:
            while True:
                try:
                    nplayer.playRandom()
                    rest = np.random.choice([1,2,4,8],1,p=[0.15,0.7,0.1,0.05])
                    time.sleep(0.25*rest[0])
                except KeyboardInterrupt:
                    exit()

if __name__ == '__main__':
    main()




