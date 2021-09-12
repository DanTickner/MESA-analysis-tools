from PIL import Image

def gif( frames_folder, frames_filenames, gif_folder, gif_filename, n_frames, frame_duration ):
	# Converts n_frames images into a gif file and saves in gif_folder.
	# n_frames = number of frames. frame_duration = time between frames in milliseconds.
	ims = []
	
	dur = [ frame_duration for n in range(n_frames) ]
	dur[-1] = dur[-1] * 5# Extend final frame
	
	for n in range( n_frames ):
		im = Image.open( frames_folder + "/" + frames_filenames + str(n+1) + ".png" )
		ims.append( im )
	
	ims[0].save( gif_folder + "/" + gif_filename + ".gif", save_all=True, append_images=ims[1:], optimize=False, duration=dur, loop=0 )
	
	return()