from fractions import Fraction as Fr
# from latex2sympy import process_sympy as pl
import sympy
from sympy.parsing.latex import parse_latex as pl
import re

test_exprns = '''\item \(\ddfrac{3}{4} * \ddfrac{1}{2} = \) \vspace{4em}
    \item \(\ddfrac{5}{7} * \ddfrac{1}{5} = \) \vspace{4em}
    \item \(\ddfrac{20}{3} * \ddfrac{6}{12} = \) \vspace{4em}
    \item \(\ddfrac{-1}{3} * \ddfrac{-9}{2} = \) \vspace{4em}
    \item \(\ddfrac{7}{3} * \ddfrac{-9}{-2} = \) \vspace{4em}
    \item \(\ddfrac{-1}{3} * \ddfrac{52}{6} = \) \vspace{4em}
    \item \(\ddfrac{3}{10} * \ddfrac{3}{11} = \) \vspace{4em}
    \item \(\ddfrac{-4}{3} * \ddfrac{3}{5} = \) \vspace{4em}
    \item \(\ddfrac{-4}{-5} * \ddfrac{-3}{7} = \) \vspace{4em}
    \item \(\ddfrac{1}{99} * \ddfrac{11}{2} = \) \vspace{4em}
    \item \(\ddfrac{-7}{3} * \ddfrac{15}{9} = \) \vspace{4em}'''

class Expression: 
    def __init__(self, string):
        self.string = string
        if '\\' in string: 
            self.string = self.tex_to_sympy(string)
    
    @classmethod
    def from_tex(cls, tex_string): 
        return cls(cls.text_to_sympy(tex_string))
        
    @staticmethod
    def tex_to_sympy(tex_string): 
        return pl(tex_string)
    
    def __repr__(self): 
        return str(self.string)
        
    def reduce(self): 
        return sympy.Rational(sympy.simplify(self.string))

    
if __name__ == '__main__': 
    # These work.  Don't know why they need a "\\" to start, while below expressions only need "\frac..."
    # ex = Expression("\\frac{d}{dx} x^{2}")
    # ex = Expression("\\frac{256}{512}")
    # print(ex.reduce())
    
    # \(, followed by any number of any character, followed by \)
    exprn = re.compile(r'\\\(.*\\\)')
    stend = re.compile(r'(\\\()|(=.*\\\))')
    ddfrac = re.compile('ddfrac')
    for item in exprn.findall(test_exprns): 
        item = stend.sub('', item)
        item = ddfrac.sub('frac', item)
        sy_exp = Expression(item)
        print(str(item) + str(sy_exp.reduce()))