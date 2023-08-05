import cv2
import win32gui, win32ui, win32con
from ctypes import windll
from PIL import Image
import numpy as np
from mss import mss

class MatchProcess():
    
    def __init__(self,large_image,small_image):
        try: self.large_image = cv2.imread(large_image) # Read the images from the file
        except: self.large_image = large_image
        try: self.small_image = cv2.imread(small_image) # Read the images from the file
        except: self.small_image = small_image
        
        method = cv2.TM_SQDIFF_NORMED
        result = cv2.matchTemplate(self.small_image, self.large_image, method)
        self.mn,_,self.mnLoc,_ = cv2.minMaxLoc(result) # min_val, max_val, min_loc, max_loc
        self.MPx,self.MPy = self.mnLoc
        self.trows,self.tcols = self.small_image.shape[:2]
    
    def judge(self,min=0.02):
        if(self.mn<min): return True
        else: return False
        
    def drawRect(self):
        cv2.rectangle(self.large_image, (self.MPx,self.MPy),(self.MPx+self.tcols,self.MPy+self.trows),(0,0,255),2)
        cv2.imwrite('match.png',self.large_image) #cv2.imshow('match',large_image), cv2.waitKey(0)
    
    def value(self):# center_pos, xywh, min_value
        return (int(self.MPx+self.tcols/2), int(self.MPy+self.trows/2)), (self.MPx, self.MPy, self.trows, self.tcols), self.mn

def match(large_image,small_image,min=0.02):
    """
    compare two images, check match or not.
    :param min: Criteria
    :param return: False or ( (center-x, center-y), (left, top, w, h), eval_min_val )
    """
    mp = MatchProcess(large_image,small_image)
    if(mp.judge(min)):
        return mp.value()
    else:
        return (-1, -1, -1)
    
def matchWithImage(large_image,small_image,min=0.02):
    """
    compare two images, check match or not.
    :param min: Criteria
    :param return: False or ( (center-x, center-y), (left-x, left-y, w, h), eval_min_val )
    generate result as 'match.png'
    """
    mp = MatchProcess(large_image,small_image)
    if(mp.judge(min)):
        mp.drawRect()
        return mp.value()
    else:
        return (-1, -1, -1)
    

def cv2toPIL(cvImage):
    img = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)
    return im_pil

def PILtocv2(pil_image):
    open_cv_image = np.array(pil_image)
    open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR 
    return open_cv_image

def windowCapture(win_name):
    
    try:
        hwnd = win32gui.FindWindowEx(None, None, None, win_name) #maplestory
    except:
        try:
            hwnd = win32gui.FindWindow(None, win_name)
        except:
            raise("can't get hwnd. sorry")
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top
    hwndDC = win32gui.GetWindowDC(hwnd)
    
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)
    saveDC=mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    saveDC.SelectObject(saveBitMap)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)
    
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        return PILtocv2(im)

def testScreen(left=0, top=0, width=300, height=300):
    while True:
        cv2.imshow('screen', windowCapture("MapleStory"))
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyAllWindows()
            break

