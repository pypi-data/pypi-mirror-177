#!/usr/bin/env python

from subprocess import call,STDOUT,check_output,run
import shutil,os,argparse,sys
import string
import pkg_resources
version= pkg_resources.require('mfig')[0].version

# How it works:
# 1. Create a tex document with necessary configurations
# 2. Compile the tex to create the pdf
# 3. Trim the pdf margins to get only the figure

class CustomParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write('\033[91mError: %s\n\033[0m' % message)
        self.print_help()
        sys.exit(2)



def createParser():
    #main parser
    parser = CustomParser(prog="onefig",formatter_class=argparse.RawTextHelpFormatter,
                          description="A tool for merging multiple figures into one.",
                          epilog="Version: {}\nCreated by Koushik Naskar (koushik.naskar9@gmail.com)".format(version)
                          )

    #adding options for numerical jobs
    parser.add_argument('-i',nargs='+',type=str,help="List of input files",metavar="FILE",required=True)
    parser.add_argument('-o',type=str,required=True,help="Output file name",metavar="FILE")
    parser.add_argument('-pr',help="Number of figure in one row (default: %(default)s)",metavar='PR',default=2,type=int)
    parser.add_argument('-it',nargs='?',choices=['b','t','n','i'],default='b',help="Where to put the caption. Available options: i, b, t, n. (default: %(default)s)",metavar='IT')
    parser.add_argument('-w',help="Width of each figure (default: %(default)s)",default=0.46,metavar='WIDTH',type=float)
    parser.add_argument('-v',help="Verticle space between rows in cm (default: %(default)s)",default=0.3,metavar='VSPACE',type=float)
    parser.add_argument('-s',nargs='+',type=str,help="Shift as (x,y) coordinate. Can be used only with inner index position",metavar="SHIFT",default=['0.1', '0.1'])
    # parser.add_argument('--rotate','-r',help="Rotate figure (default: %(default)s)",default=0,metavar='ROTATE',type=float)

    return parser.parse_args()


def main():
    args = createParser()
    createPdf(args)


def createPdf(args):
    destDir = 'tmp_pdfmerger'
    os.makedirs(destDir,exist_ok=True)

    for file in args.i:
        shutil.copy(file, destDir)

    os.chdir(destDir)
    tex = createTeX(args)
    with open('test.tex','w') as f:
        f.write(tex)

    try:
        with open('tmp.log','a') as f:
            ret = run(['pdflatex', '-halt-on-error', '-interaction=nonstopmode','test.tex'],stdout=f,stderr=STDOUT,timeout=5)
            if ret !=0:
                raise Exception("Failed to compile pdf. Make sure all the packages are properly installed")

            ret = run(['pdfcrop','test.pdf','../{}'.format(args.o)],stdout=f,stderr=STDOUT,timeout=9)
            if ret !=0:
                raise Exception("Failed to crop pdf. Make sure 'pdfcrop' is installed")
    except :    
        raise
    finally:
        os.chdir('../')
        shutil.rmtree(destDir)





def createInnerIndex(ifiles,iRow,width,shift):

    charGen = (x for x in string.ascii_lowercase)

    fig = ''
    for ind,elem in enumerate(ifiles,start=1):
        fig += r'\subfloat{\tikz{\node (a) {\includegraphics{'+elem+r'}};'
        fig+=r'\node[below right of=a, xshift='+shift[0]+'cm, yshift='+shift[1]+r'cm] at (a.north west) {\footnotesize('+next(charGen)+r')}; }}'
        fig += r'\\' if not ind%iRow else r"\hfill"
        fig +='\n'



    txt = r'''
    \documentclass[a4,12pt]{article}
    \usepackage{graphicx}
    \usepackage{subfig}
    \usepackage{tikz}
    \thispagestyle{empty}


    \begin{document}


    \begin{figure}
    \tikzset{inner sep=0pt}
    \setkeys{Gin}{width='''+width+r'''\textwidth}
    \centering

    '''+fig+r'''


    \end{figure}
    \end{document}

    '''
    return txt



def createOuterIndex(iFiles,iRow,iType,vSpace,width):

    thisFig = {
        'b':r'\subfloat[]',
        't':r'\sidesubfloat[]',
        'n':r'\subfloat'
    }[iType]

    fig = ''
    for ind,elem in enumerate(iFiles,start=1):
        fig += thisFig+r'{\includegraphics[width=\imsize]{'+elem+'}}'
        fig += r'\\\vspace{'+vSpace+'cm}' if not ind%iRow else r"\hfill"
        fig +='\n'

    figWidth = r"\newcommand{\imsize}{"+width+r"\textwidth}"

    txt =  r'''
    \documentclass[a4,12pt]{article}
    \usepackage[a4paper,margin=0in]{geometry}

    \usepackage{subfig}
    \usepackage{graphicx}
    \usepackage{multirow}
    \usepackage{floatrow}

    \thispagestyle{empty}


    \captionsetup[subfigure]{justification=raggedright,farskip=12pt,captionskip=12pt,position=auto,labelfont=bf}
    \floatsetup[figure]{style=plain,subcapbesideposition=top}

    '''+figWidth+r'''
    \begin{document}

    \begin{figure}[!htp]
    \centering


    '''+fig+r'''\end{figure}\end{document}'''

    return txt




def createTeX(args):
    inOneRow=args.pr
    width = args.w
    ifile = args.i
    iType = args.it
    shift = args.s
    assert len(shift)==2, "A pair of x,y coordinate is required"

    assert (1.0/inOneRow)>width, "Width {} is too large to fit {} figure in one row".format(width,inOneRow)

    width = str(width)

    if iType=='i':
        return createInnerIndex(ifile,inOneRow,width,shift)
    else:
        return createOuterIndex(ifile,inOneRow,iType,str(args.v),width)




if __name__ =="__main__":
    main()
