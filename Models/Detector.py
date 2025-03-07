import cv2 #Import computer vision to process video (its in the open AI github accessed online)
import numpy as np #Numpy is also accessed online and is for 
import time 
class Detector:
    def __init__(self, videoPath, configPath , modelPath, classesPath):
        self.videoPath = videoPath #Establishing an connection to the video 
        self.configPath = configPath #Still establishing a connection but i lowk dont even know what a configuration file is in this context 
        self.modelPath = modelPath #Path to the trained model (from the internet) 
        self.classesPath = classesPath #Also a path but I lowk dont know what differentiates the classes it can access and cant 

        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath) #Takes the paths as parameters to access the models 
        self.net.setInputSize(320,320) #The following lines sets various values of the video such as size and red/blue switches 
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)
        
        self.readClasses() #Sets up a line of code 

    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        
        self.classesList.insert(0, '__Background__')
        self.colorList  = np.random.uniform(low = 0, high = 255, size = (len(self.classesList), 3))

        print(self.classesList)  

    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)  #Opens the video file 
        if (cap.isOpened()==False): 
            print("Error")
            return 
        
        (success,image) = cap.read() 

        zeroSpeedTime = 0 #Straight up just defining it as 0 for the initial runthrough 

        while success: #Bounded Box creating stuff 
            currentTime = time.time()
            fps = 1/(currentTime - zeroSpeedTime)   #How am I even assuming its 1 frame per runthrough
            zeroSpeedTime = currentTime #On second runthrough so it no longer uses the 0 value 
            classLabelIDs, confidences, bboxs =  self.net.detect(image, confThreshold = 0.5) #Reads every frame one by one and checks if it bypasses the confidence threshold, basically saying, aight that looks good enough 
            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1,-1)[0]) #Just in case it doesnt format properly, it puts it in a list of confidences
            confidences = list(map(float, confidences)) #Converts it to float and applies it to every confidence through the map function 

            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold = 0.5, nms_threshold = 0.2) #Breaking it up into a bunch of different boxes that square around everything 
            #Prevents overlapping boxes with this function 
            if len(bboxIdx) != 0: 
                for i in range(0,len(bboxIdx)): 
                    bbox = bboxs[np.squeeze(bboxIdx[i])] #Reading the specific index of the list (extracting it) 
                    classConfidence = confidences[np.squeeze(bboxIdx[i])] #Formatting so it doesnt mess up the code 
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])]) #Formatting it so it doesnt mess up the code 
                    classLabel = self.classesList[classLabelID]
                    classColor = [int(c) for c in self.colorList[classLabelID]] #Gotta do it like this if you arent limiting the previous
                    fps = int(fps)
                    textDisplay = str((classLabel,fps)) 
                    x,y,w,h = bbox #Defined by the bbox variable
                    cv2.rectangle(image, (x,y), (x+w, y+h), color=classColor, thickness=2) #Finding the x and y coordinates of the bounding boxes #Its to get all 4 corners of the bounding box, but why does this matter, setting the color of the box to white
                    cv2.putText(image, textDisplay, (x,y), cv2.FONT_ITALIC, 1,color = (0,165,255))
                    global newX #In order to access these variables outside of this particular method 
                    newX = x
                    global newY
                    newY = y
                    global column
                    global row
                    newWidth = 1920
                    newHeight = 1080
                    widthGrid = newWidth/4 
                    widthHeight = newHeight/4
                    A = (newWidth/4)*1
                    B = (newWidth/4)*2
                    C = (newWidth/4)*3
                    D = (newWidth/4)*4
                    One = (newHeight/4)*1
                    Two = (newHeight/4)*2
                    Three = (newHeight/4)*3
                    Four = (newHeight/4)*4
                    if newX < A and newY < One:
                        column = 1
                        row = 1
                    elif newX < B and newY < One:
                        column = 2
                        row = 1
                    elif newX < C and newY < One:
                        column = 3
                        row = 1
                    elif newX < D and newY < One:
                        column = 4
                        row = 1
                    elif newX < A and newY < Two:
                        column = 1
                        row = 2 
                    elif newX < B and newY < Two:
                        column = 2
                        row = 2
                    elif newX < C and newY < Two:
                        column = 3
                        row = 2 
                    elif newX < D and newY < Two:
                        column = 4
                        row = 2 
                    elif newX < A and newY < Three:
                        column = 1
                        row = 3
                    elif newX < B and newY < Three:
                        column = 2
                        row = 3 
                    elif newX < C and newY < Three:
                        column = 3
                        row = 3 
                    elif newX < D and newY < Three:
                        column = 4
                        row = 3
                    elif newX < A and newY < Four:
                        column = 1
                        row = 4
                    elif newX < B and newY < Four:
                        column = 2
                        row = 4
                    elif newX < C and newY < Four:
                        column = 3
                        row = 4
                    elif newX < D and newY < Four:
                        column = 4
                        row = 4
                    global grid
                    grid = [[' ' for i in range(4)] for i in range (4)] #Will basically set up an empty space grid with an array 
                    if classLabel == "car":
                        grid[column-1][row-1] = "*" #Represented by 1 poke 
                    if classLabel == "person":
                        grid[column-1][row-1] = "O" #Represented by 3 pokes 
                    if classLabel != "car" and classLabel != "person": 
                        grid[column-1][row-1] = "+" #Represented by 2 pokes 
                    print(grid[0])
                    print(grid[1])
                    print(grid[2])
                    print(grid[3])
                    print(" ")
                    print(" ")

            cv2.imshow("Result", image) #Prints the rectangle put around the bounding box 
            
            key = cv2.waitKey(1) & 0xFF #Idk what the 0xFF means, but the loop is to keep checking each frame until you hit quit 
            if key == ord("q"):
                break 

            (success, image) = cap.read() #If the previous loop was not broken, then its just gonna move on to the next frame in the video and check everything again
        cv2.destroyAllWindows #To shut down everything in the event of q being hit 

    def measuringFunction():
        global column
        global row
        newWidth = 1920
        newHeight = 1080
        widthGrid = newWidth/4 
        widthHeight = newHeight/4
        A = (newWidth/4)*1
        B = (newWidth/4)*2
        C = (newWidth/4)*3
        D = (newWidth/4)*4
        One = (newHeight/4)*1
        Two = (newHeight/4)*2
        Three = (newHeight/4)*3
        Four = (newHeight/4)*4
        if newX < A and newY < One:
            column = 1
            row = 1
        elif newX < B and newY < One:
            column = 2
            row = 1
        elif newX < C and newY < One:
            column = 3
            row = 1
        elif newX < D and newY < One:
            column = 4
            row = 1
        elif newX < A and newY < Two:
            column = 1
            row = 2 
        elif newX < B and newY < Two:
            column = 2
            row = 2
        elif newX < C and newY < Two:
            column = 3
            row = 2 
        elif newX < D and newY < Two:
            column = 4
            row = 2 
        elif newX < A and newY < Three:
            column = 1
            row = 3
        elif newX < B and newY < Three:
            column = 2
            row = 3 
        elif newX < C and newY < Three:
            column = 3
            row = 3 
        elif newX < D and newY < Three:
            column = 4
            row = 3
        elif newX < A and newY < Four:
            column = 1
            row = 4
        elif newX < B and newY < Four:
            column = 2
            row = 4
        elif newX < C and newY < Four:
            column = 3
            row = 4
        elif newX < D and newY < Four:
            column = 4
            row = 4
    def grid():
        global grid
        grid = [[' ' for i in range(4)] for i in range (4)] #Will basically set up an empty space grid with an array 
        return grid 
    def pickSpot(column, grid, row):
        grid[column][row] = "*"

    
        


