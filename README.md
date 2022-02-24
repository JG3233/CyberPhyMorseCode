# CyberPhyMorseCode

A repo for developing a cyber physical channel.

## Covert Design Overview

The goal of this covert channel is to exfiltrate messages from a building using visual signals. Our covert channel uses a smartphone Morse code converter application to encode and transmit Morse code messages through the use of the phone's flashlight. 

In order to build this channel the transmitter must have a smartphone with the Morse Code Converter App installed, as well as access to a window through which the encoded message can be flashed to a receiver outside. The receiver must have access to a video recording device as well as our decoding script and the necessary dependencies. The methodology of the scripts is to extract translate the video to images. The brightness of the images is then used to construct the Morse code and decode the message.

## Implementation and Experiment

Since we decided to pursue the Morse code cyber-physical channel, there were skeleton functions written for us to develop into a working prototype. Here we can describe each step individually, including the goals of the step and how we achieved those goals.

### Converting the Video into Frames

The first step was to read in the video by passing in a path and produce frames that can be analyzed individually. To complete this step, we utililzed the cv2 library. The library turns the path into a video object that we could then call read() on. This gave us a frame which could then be written to the output folder created by os.mkdir(). During the writing process we kept a count of the number of frames, which the video_to_images function returns.

### Extracting Physical Signals

Now that we have a number of frames to analyze, we need to extract the physical signals given in the video. The brightness function performs this task by leveraging the PIL Image and ImageStat libraries. Using Image.open to analyze the frame passed into brightness, we could take the mean RGB value of the whole image using ImageStat.Stat(im).mean, which returns a list [R,G,B] where each value varies from 0-255, of each frame. To further distill the brightness, we averaged out the 3 values to produce a single brightness metric.

### Convert Physical Signals into Lengths

Up to this point we have successfully converted our video into frames, for each we calculate a brightness metric. By performing this process on each frame and collecting the brightness values in a chronological list, we can then use the brightness_to_length function to interpret how long the signals were present. For instance, since morse code differentiates dots and dashes by how long the flashlight shines, we need to distinguish between these two signals. Our technique was to produce an array that reflected lengths of brightness and darkness as positive and negative values respectively. 

Another important part of determining lengths was to establish a threshold for what constitutes a bright/dark frame. We accomplished this with the help of a helper function get_brightness_threshold, which attempts to filter out peaks using a rolling average of the maximum and minimum brightness detected in the frames. This way we were able to more reliably measure what constitutes a bright and dark frame, measuring the threshold as precisely the average.

Once a threshold is established, we can then create signal lengths by creating a new entry in the list for changes from dark to light or vice versa. If the frame is the same brightness category as the previous, we simpy increment/decrement the previous entry to reflect consecutive frames of the same category (1 -> 2 or -1 -> -2). This technique allows us to return a list of signal lengths that accurately reflects the length of a light or dark symbol by the number of frames that evaluate to said category. We can also trim edge darkness by removing negative first and last values in the array since the message begins and ends with bright symbols.

### Classify Signal lengths as Symbols

Using signal lengths, we can then determine which symbol was intended, thanks to the rules of Morse code using nonconsecutive units (1,3,7). First, we calculated the number of frames in a single unit with another helper function. This is particularly helpful for changes in pacing when transmitting the message via Morse code. To calulate the length of a unit, the helper function calculate_unit_length simply takes the absolute value of each signal length and returns the most common occurence (the mode). We can reliably determine the smallest unit this way since Morse code spaces out each signal in a letter with a single unit of darkness. Dots are a single unit of brightness, and together they constitute the most common symbols. 

Once we can deduce the unit length, classifying symbols is simply a matter of establishing ranges. Anything less than 2 units is a 1 unit symbol, darkness being between letters and brightness being a dot. To find 3 unit symbols we used the 2-5 unit category, finding both dashes and spaces between letters. Finally, dark values larger than 5 units were the 7 unit darkness that reflects spaces between words. To reflect each symbol we can simply use the numbers 0,1,2,3,4 as suggested.

0: space_between_words  
1: space_between_letters    
2: space_in_letter  
3: dot  
4: dash 

### Parse Symbols and Convert from Morse Code to Plaintext

Now that we have all of our Morse symbols, we simply need to collect dots and dashes until there is a space between words (or the message ends), effectively ignoring spaces between parts of the same letter. Once on of these occurs, we can convert the dots and dashes to a letter with the morse_to_letter dictionary. Next, we add the letter to the plaintext and reset the dots and dashes of the current letter to empty. 

Running through the list of symbols, we can produce a plaintext message that decodes the Morse code in the original video! We also recognized that any incorrectly determined letters would break the decoder. We also discuss this in the next section, but we introduced some robustness by detecting incorrect calls to the dictionary and indicating a wrong character and setting a flag that would wait until the next space character to continue decoding.

## Conclusion and Future Direction

*in progress*
