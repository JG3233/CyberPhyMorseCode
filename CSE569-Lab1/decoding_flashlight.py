### pip3 install opencv-python
### pip3 install pillow
### pip3 install matplotlib
### pip3 install ckwrap
### pip3 install bcrypt

import cv2
import os
import ckwrap
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageStat

""" 
    Part 1. Identify Physical Signals.
"""

def video_to_images(input_video_path, output_folder_dir):
    """
        Description: Convert input video to images of each frame and calculate 
                     the total number of frames in the input video.
        Input: 
            - input_video_path: path of input video.
            - output_folder_path: the path of the folder that stores image of each frame.
        Output: 
            - Number of frames the input video generated (Return Value).
            - A folder that contains all frame images of the input video.
        Libraries you may need: 
            - cv2.VideoCapture()
            - os
    """
    # Your code starts here:
    video = cv2.VideoCapture(input_video_path)
    res, img = video.read()
    os.mkdir(output_folder_dir)
    frames = 0
    while res:
        cv2.imwrite(output_folder_dir + '/frame' + str(frames) + '.jpg', img)
        res, img = video.read()
        frames += 1

    return frames

def brightness(im_file):
    """
        Description: Calculate the brightness of input image. 
        Input: 
            - im_file: path of the image.
        Output(Return Value): 
            - Return the brightness of input image.
        Libraries you may need: 
            - Image
            - ImageStat
    """
    # Your code starts here:
    with Image.open(im_file) as im:
        bright_list = ImageStat.Stat(im).mean
        avg_img_bright = sum(bright_list) / len(bright_list)
    
    return avg_img_bright

def plot_brightness(x, y):
    """ Plot the brightness of each frame. """
    plt.figure(figsize=(15,5))
    plt.title('Brightness per Frame',fontsize=20)
    plt.xlabel(u'frame',fontsize=14)
    plt.ylabel(u'brightness',fontsize=14)
    plt.plot(x, y)
    plt.show()

""" 
    Part 2. Convert Physical Signals to Digital Signals.
"""

def brightness_to_lengths(threshold, brightness_per_frame):
    """
        Description: Calculate lengths of consistent signals.
        Input: 
            - threshold: a value of brightness that distinguishes light frames from dark ones.
            - brightness_per_frame: a list of brightness values of all frames.
        Output: 
            - A list of signal lengths (Return Value)
        Libraries you may need: N/A
    """
    # Your code starts here:
    sig_lens = []
    for i in range(0, len(brightness_per_frame)):
        if brightness_per_frame[i] > threshold:
            if i > 0 and sig_lens[len(sig_lens) - 1] > 0:
                sig_lens[len(sig_lens) - 1] += 1
            else:
                sig_lens.append(1)
        else:
            if i > 0 and sig_lens[len(sig_lens) - 1] < 0:
                sig_lens[len(sig_lens) - 1] -= 1
            else:
                sig_lens.append(-1)
    
    if sig_lens[0] < 0:
        sig_lens = sig_lens[1:]
    
    if sig_lens[len(sig_lens) - 1] < 0:
        sig_lens = sig_lens[:-1]
    
    return sig_lens
            
def classify_symbols(symbols):
    """
        Description: Due to the minor errors during the flashlight generating 
        and converting processes, the length of a symbol we calculate in 
        the last step is more likely to be a range than a certain value. 
        Implement the classify_symbols(symbols) function that labels 
        each length to a Morse symbol.
        Input: 
            - symbols: a list of signal lengths
        Output: 
            - A list of signal labels (Return Value)
        Libraries you may need: ckwrap.ckmeans
    """
    # Your code starts here:
    sig_labs = []
    for i in range(0, len(symbols)):
        if symbols[i] < -60:
            sig_labs.append('0')
        elif symbols[i] < -40:
            sig_labs.append('1')
        elif symbols[i] < -10 and symbols[i] > -40:
            sig_labs.append('2')
        elif symbols[i] > 10 and symbols[i] < 40:
            sig_labs.append('3')
        elif symbols[i] > 40:
            sig_labs.append('4')
    
    return sig_labs

"""
    Part 3. Convert Morse Code to Plaintext
"""

morse_to_letter = {'.-':'A', '-...':'B', '-.-.':'C', '-..':'D', '.': 'E', '..-.':'F', '--.':'G',
                   '....':'H', '..':'I', '.---':'J', '-.-':'K', '.-..':'L', '--':'M', '-.':'N',
                   '---':'O', '.--.':'P', '--.-':'Q', '.-.':'R', '...':'S', '-':'T', 
                   '..-':'U', '...-':'V', '.--':'W', '-..-':'X', '-.--':'Y', '--..':'Z',
                   '.-.-.-':'.', '--..--':',', '-.-.--':'!', '..--..':'?', '-..-.':'/', '.--.-.':'@', '.----.':'\'',
                   '.----':'1', '..---':'2', '...--':'3', '....-':'4', '.....':'5',
                   '-....':'6', '--...':'7', '---..':'8', '----.':'9', '-----':'0'}

def morse_to_plaintext(morse):
    """
        Description: Convert Morse code to plaintext
        Input: 
            - morse: a list of labels, each label is a number that represents a kind of Morse Code.
              e.g. [3,2,3,1,4,2,3], where 
              0: space_between_words
              1: space_between_letters
              2: space_in_letter
              3: dot
              4: dash
        Output(Return Value): 
            - a plaintext sentence string
        Libraries you may need: N/A
    """
    # Your code starts here:
    pt = ''
    cur = ''
    for i in range(0,len(morse)):
        if morse[i] == '0':
            pt += morse_to_letter[cur] + ' '
            cur = ''
        elif morse[i] == '1':
            pt += morse_to_letter[cur]
            cur = ''
        elif morse[i] == '3':
            cur += '.'
            if i == len(morse) - 1:
                pt += morse_to_letter[cur]
        elif morse[i] == '4':
            cur += '-'
            if i == len(morse) - 1:
                pt += morse_to_letter[cur]
    
    return pt

"""
    Part 4. Compile all above steps togther.
"""
def run(input_dir):
    # Part 1
    output_name = input_dir.split('.')[0].split('/')[1]
    output_dir = 'outputs/'+output_name+'_output'
    # Your code starts here:
    # num_imgs = video_to_images(input_dir, output_dir)
    num_imgs = 3182 # temp to not recalc images ^
    brightness_array = [None] * num_imgs
    for i in range(0,num_imgs):
        img_brightness = brightness(output_dir + '/frame' + str(i) + '.jpg')
        brightness_array[i] = img_brightness

    # print("\nCheckpoint 1: brightness plot")
    # plot_brightness(range(num_imgs), brightness_array)
    
    # Part 2
    # Your code starts here:
    signal_lengths = brightness_to_lengths(100, brightness_array)
    # print("\nCheckpoint 2: a list of signal lengths is ", signal_lengths)
    signal_labels = classify_symbols(signal_lengths)
    # print("A labeled list of signals is ", signal_labels)

    # Part 3
    # Your code starts here:
    plaintext = morse_to_plaintext(signal_labels)
    print("\nCheckpoint 3: The plaintext is ", plaintext)
    return plaintext

run('inputs/encoded.mov')