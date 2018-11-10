import pysynth as ps

freqs = ps.getfreq()
notes = freqs[0].keys()
for n in notes:
    outfile = 'wav/%s.wav' % n
    ps.make_wav( ((n, 4),), fn=outfile)
    print( 'Wrote note %s to %s' %(n, outfile) )
