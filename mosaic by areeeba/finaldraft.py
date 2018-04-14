import matplotlib.pyplot as plt 
import PIL.Image as Image
import os.path
import PIL.ImageDraw as ID
import numpy as np
import os
import math
#--------------------------------------------------------------------------
def get_flower(red,green,blue,colors): # loop which compares the averages
    summ=0
    match=0
    smol=100000000
    for repeat in range(len(colors)): #this loop gets the sum of the difference between each RGB values from the average values of the small images squared. 
        summ=(abs(red-(colors[repeat][0])))**2+(abs(green-(colors[repeat][1])))**2+(abs(blue-(colors[repeat][2])))**2 #the greater this power, the more precise the colors
        # it is squared to give more magnified differences. the greater the power the more precise it becomes; however too much 
        #will results blank spaces for not all the possible colors are there. Adding more images and increasing the power will make it more precise as well. 
        if summ<smol:
            match=repeat
            smol=summ
    return (match)
    
def mosaic(image_name,new_name, precision):
    print ("Process Has Began!")
    '''Enter the name of the .jpg image file (string form) you would like to 
    apply this mosaic effect on. Input image larger than 1920x1080 recommended 
    but all size of images can work. Insert the new name of the image you would
    like to save it as  in non  -.jpg format. In the third argument, put integer
    1 to get medium precision and 0 for max precision.'''
    
    #before use, the file you'd like to edit must be a jpg.
    #it should be in the same folder as this file
    #the newly edited file will be saved in CD
    
    #List/ints for later use to store data.
    picn=1 # this variable helps collect certain images from the file
    colors=[] # this list stores the average RBG color scheme for each of the small 3283 photos.
    #this will be later used to compare each of these averages to sections of orignal image to paste on a mask.
    filesname=[] # this stores the name of the file, so it can be called later when the match is found
    listue=[] #this list #2 helps append a the list of average RBG of small photos to the list of colors
    pixle=0 #i know this is spelled wrong but this variable helps keep tract of RBG averages, and append to the list:"listue"

    directory=os.path.dirname(os.path.abspath(__file__)) #gets the directory of this file
    filename2=os.path.join(directory, str(image_name)) # creates file path for the image name given by the user
    file3=Image.open(filename2) #opens the given image

    org_width, org_height = file3.size # this stores the height and the width of the given file.

    if precision == 0:
    	smallimg_wh = 30 #small images width and height (either 20x20 or 30x30 depending on input)
    	small_image_name = "flower1_" #images with int 1 after the flower are 30x30 images
    	smallimg_div_y = math.floor(org_height/30) #this is the amount of time the 30x30 images will fit onto the height of the screen
    	smallimg_div_x = math.floor(org_width/30) #this is the amount of time the 30x30 images will fit onto the width of the screen
    	average_sum = 900 # this is the denominator for 30x30 process for getting averages of the small sections of original image.
    else:
    	small_image_name = "flower_" #these are all 20x20 
    	smallimg_wh = 20
    	smallimg_div_y = math.floor(org_height/20) #this is the amount of time the 20x20 images will fit onto the height of the screen
    	smallimg_div_x = math.floor(org_width/20) #this is the amount of time the 20x20 images will fit onto the width of the screen
    	average_sum = 400 # this is the denominator for 20x20 process for getting averages of the small sections of original image.
    	#the smaller the smaller images of flower, the more precise the results.
    
    	
    for i in range(3283): #records the names/color composition of all photos in the project   
        n=str(picn) #this is the picture number 
       	n=(n.zfill(4)) #fills intergers to 4 digits: ie. from 4 to 0004 or from 10 to 0010 etx
       	filename1=os.path.join(directory, small_image_name +n+'.jpg') #filepath
       	content1=plt.imread(filename1) #this allows us to examine/store/compare the pixels of the smaller images.
       	for n in (0,1,2): # this loop gets the small pictures color composition
            for p in range (smallimg_wh): #this loop is for adding up all the pixels of one small image and storing it.
               for q in range (smallimg_wh):
                   pixle+=content1[p][q][n]
            pixle=round(pixle/400) # gets the average color comp of each color RBG individually
            listue.append(pixle) #stores in a list i.e listue = [R,G,B]
            pixle=0 #int pixle is emtied for reuse
        colors.append(listue) #listue is appened to colors ie. [[R,G,B],[R,G,B]...]
        listue=[] #listue is cleared for reuse
        filesname.append(filename1) #the file's path is appended here to be able to recall it later if it matches.
        picn+=1 # this changes the number in the names of the small images being scanned,allowing this loop to go through all the images. 
        
    print ("COLORS LIST HAS BEEN CREATED")
    
    filename2=os.path.join(directory, str(image_name)) # creates file path for the image name given by the user
    
    file3=Image.open(filename2) #opens the given image
    org_width, org_height = file3.size # this stores the height and the width of the given file.
    
    #the following if statement will determine the preciseness of the image to the users content and set up some variables
    
    
    content2=plt.imread(filename2) #opens the dictionary of the color contents of the image

    
    pixel,summ,smol = 0,0,10000 #randon by important variables which will help compare the small
    #images content to the sections of the original ones.
    match=0 # this is important: after doing all the calculations and comparing the colors list of the small image's contents
    #a function will send an index number of the most fitting small image to be pasted on a Mask.
    
    w,h=0,0 # this is something i cannot tell
    red,green,blue=0,0,0 #
    
    Mask=Image.new('RGBA',(org_width,org_height),(0,0,0,0)) #creates a new transparent mask to paste the matched photos on.
    
    #miniv=20
    listue1=[] # another list 
    
    print ("PICTURE MATHCHING STARTS NOW")
    
    for y in range(smallimg_div_y): # this loop scans 20x20 or 30x30 sections of the original image, recording their color contents as well
        for z in range(smallimg_div_x):
            summ,smol=0,10000
            for a in range(smallimg_wh): 
                for b in range(smallimg_wh): 
                    red += (content2[a+y*smallimg_wh][b+z*smallimg_wh][0]) # content2 is the color content list of the original 1920x1080 image
                    green += (content2[a+y*smallimg_wh][b+z*smallimg_wh][1])
                    blue += (content2[a+y*smallimg_wh][b+z*smallimg_wh][2])

            red=round(red/average_sum)
            green=round(green/average_sum) # color average for each section
            blue=round(blue/average_sum)
            wid=smallimg_wh*z  # helps find the place where this new match needs to be pasted
            hei=smallimg_wh*y
            match=get_flower(red,green,blue,colors) # a function which compares the colors list to the RGB average from original image's sections. 
            file1=Image.open(filesname[match]) #opens the image which matches the best 
            Mask.paste(file1,(wid,hei)) # pastes the image on the mask at a certain position
    print ("MATCHING")
            
    fig,ax=plt.subplots(1,2) # creates the gird which displays the images
    
    ax[0].imshow(file3)
    ax[1].imshow(Mask)
    #ax[2].imshow(file1)
    
    fig.show()
    
    Mask.save(new_name+".jpg")
    
    print("Image saved :)")
    #image is saved to the current directory


                        
            
