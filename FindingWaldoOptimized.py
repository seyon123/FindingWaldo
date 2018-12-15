#Name: Seyon Rajagopal
#Description: This program is a much more faster version of the other finding waldo program.
#             It searches finds waldo given a scene. It takes in both an image of waldo and
#             an image of the scene to look in and then outputs the scene with a box around 
#             where waldo is. It takes approx takes 4-5min to finish on the larger image

#importing clock to find the time taken
from time import clock

#setting media path and defining images 
setMediaPath(getMediaPath())
bigScene = makePicture('scene.jpg')
smallScene = makePicture('tinyscene.jpg')
bigWaldo = makePicture('waldo.jpg')
smallWaldo = makePicture('tinywaldo.jpg')

#Function that looks at the template and the search image at a specific x1 and y1 and 
#calulates the SAD value at that point
def compareOne(template, searchImage, x1, y1):
  W = getWidth(template)
  H = getHeight(template)
  
  #increment value that increments every width/2 
  increment = W/2
  
  sum = 0
  #only get luminance values for those in in range of the increment
  for x in range(0,W,increment):
    for y in range(0,H,increment):
      pixel = getPixel(template,x,y)
      #any component of color would have the same luminance value so it is fine to just take the value from red
      luminance1 = getRed(pixel)
      pixel2 = getPixel(searchImage,x1 + x,y1 + y)
      luminance2 = getRed(pixel2)
      #calculating sum of the absolute value of the differences in luminance
      sum += abs(int(luminance2)-int(luminance1))
  return sum

#Function that keeps runing compareOne on every pixel within the searchImage and returns a matrix of compareOne values  
def compareAll(template, searchImage):
  W1 = getWidth(template) 
  W2 = getWidth(searchImage) 
  H1 = getHeight(template) 
  H2 = getHeight(searchImage) 
  
  #creating a matrix of values for all pixels in the search image of sithe same size as the search image  
  matrix = [[999999 for i in range(W2)] for j in range(H2)]
  
  #setting a limit for the search to occur so the search doesnt go beyond 
  #the size of the template as it goes through all the pixels in the picture
  for x in range (W2 - W1 + 1):
    for y in range(H2 - H1 + 1):
      luminance = compareOne(template,searchImage,x,y)
      matrix[y][x] = luminance 
  return matrix

#Function that returns the coordinate where the value is a minimum (minrow,mincol)      
def find2Dmin(matrix):
  mincol = 0
  minrow = 0
  for i in range(0,len(matrix)):
    for j in range(0,len(matrix[i])):
      #compare between current and previous value to see which is minimum
      check = min(matrix[i][j] , matrix[i-1][j-1])
      #checks to see whether or not the current minimum is smaller than the last saved minimum if it is save that
      if check < matrix[mincol][minrow]:
        minrow = j
        mincol = i
  return(minrow,mincol)

#Function that displays a box around waldo when he is found   
def displayMatch(searchImage, x1, y1, w1, h1, color):
  H = h1
  W = w1
  border = 3
  for x in range(x1,W + x1):
    for y in range(y1,H + y1):
      if x not in range(x1 + border, W + x1 - border): 
        pixel = getPixel(searchImage,x,y)
        setColor(pixel,color)
      if y not in range(y1 + border, H + y1 - border):
        pixel = getPixel(searchImage,x,y)
        setColor(pixel,color)     
  return searchImage

#Function thats greyscales the image
def grayscale(picture):
  W = getWidth(picture)
  H = getHeight(picture)
  for x in range(W):
    for y in range(H):
      pixel = getPixel(picture,x,y)
      r = getRed(pixel)
      g = getGreen(pixel)
      b = getBlue(pixel)
      luminance = (r + g + b)/3
      luminanceColor = makeColor(luminance,luminance,luminance)
      setColor(pixel,luminanceColor)
  return picture

#Main function that runs all the helper functions to find waldo and outputs the time taken  
def findWaldo(gTarget, gSearch):
  #starting time
  t1 = clock()
  
  #run the functions required to find waldo
  gTarget = grayscale(gTarget)
  gSearch = grayscale(gSearch)
  matrix = compareAll(gTarget,gSearch)
  minx,miny = find2Dmin(matrix)
  displayMatch(gSearch, minx, miny, getWidth(gTarget), getHeight(gTarget), red)
  
  #computing time taken and outputting it
  t2 = clock()
  time = t2-t1
  m, s = divmod(time, 60)
  h, m = divmod(m, 60)
  print "The program finished in: " + "%d:%02d:%02d" % (h, m, s,) + "(h, m, s,)"  
  
  #show the final image
  explore(gSearch)

#Set media path to folder with images : setMediaPath()
#Run File by running: findWaldo(bigWaldo, bigScene)
