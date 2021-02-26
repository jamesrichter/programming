import cv2
import numpy as np

# a = np.array([[0,1,1,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]])
# b = np.array([[0,1],[0,1]])
# mask = np.array([[0,1],[0,1]])
# b = np.array([[0,0,0,1],[0,0,0,1]])
# mask = np.array([[0,0,0,1],[0,0,0,1]])

# a = np.array([[ 24, 136,   0,  17,  42],
#        [181, 150, 157, 205, 109],
#        [180, 124, 122,  58,  71],
#        [170,   3, 153, 252,  32],
#        [ 15,  98, 173,  77, 162]], dtype=np.uint8)

# b = np.array([[32,170],[162,15]], dtype=np.uint8)

# # trimming the object to the smallest it can be
# brect = cv2.boundingRect(mask.astype(np.uint8))
# r = brect
# mask = mask[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
# b = b[r[1]:r[1]+r[3],r[0]:r[0]+r[2]]
# print(mask, b)

# # matching the object to the larger image
# res = cv2.matchTemplate(a.astype(np.uint8), b.astype(np.uint8), cv2.TM_CCORR_NORMED, mask=mask)

# #TODO FIND OBJECTS CUT OFF BY EDGE OF SCREEN

# res == 1
# # find the sub objects and take the AND/union of subs + res
# new = np.zeros(res.shape)


# # first you have to add extra 1s to cover the res mask
# a = array([[[ 88,  88,  88,  88],
#         [ 88,  88,  88,  88]],

#        [[148, 148, 148, 148],
#         [148, 148, 148, 148]],

#        [[248, 248, 248, 248],
#         [248, 248, 248, 248]]], dtype=uint8)
# m = array([[1, 0, 0, 0],
#        [1, 1, 1, 1]], dtype=uint8)




a = np.array([[[ 88, 148, 248],],
 [[ 88, 148, 248]],
 [[ 88, 148, 248]]] )
b = np.array([[1.],
 [1.],
 [1.]])

import numpy as np
z=np.array([[[ 88, 148, 248],
       [ 88, 148, 248],
       [ 88, 148, 248],
       [ 88, 148, 248]],
       [[ 58, 148, 248],
       [ 58, 148, 248],
       [ 58, 148, 248],
       [ 58, 148, 248]]], dtype=np.uint8)
a=np.array([[[ 88, 148, 248],
       [ 88, 148, 248],
       [ 88, 148, 248],
       [ 88, 148, 248]]], dtype=np.uint8)
b=np.array([[1,1,1,1]], dtype=np.uint8)

b = np.stack([b,b,b], axis=-1)

print(z.shape, a.shape, b.shape)
res = cv2.matchTemplate(z, a, cv2.TM_SQDIFF, 
                            mask=b)
print("asdf", res)


# sha/dty (3, 1, 4) uint8





# def create_mask():
#     clear_all_rects()
#     mask = mask_from_coords(object_pixels)
#     add_template(mask)
#     outline_found_mask(mask)
#     print(all_rects)

# def show_found_objects():    
#     # matching the object to the larger image
#     reses = []
#     for i in templates:
#         tmask = np.zeros((240,224))
#         print(repr(i[:,:,:3]))
#         print(repr(i[:,:,3]))
#         b = i[:,:,3]
#         b = np.stack([b,b,b], axis=-1)
#         founds = find_template_in_image(array, i[:,:,:3], b)
#         # print("array", array)
#         # print()
#         # print("fsum", founds.sum(),)
#         # print(repr(array))
#         # print(list(zip(*np.where(founds==1))))
#         mshape = i[:,:,3].shape
#         #need to make big mask out of small mask + coordinates
#         coords = list(zip(*np.where(founds==1)))
#         for x in coords:
#             tmask[x[0]:x[0]+mshape[0], x[1]:x[1]+mshape[1]] = i[3]
#         outline_found_mask(tmask, color='yellow')