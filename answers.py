import sympy
from sympy.parsing.latex import parse_latex as pl
import re
import sys
# useful alternatives: 
# from fractions import Fraction as Fr
# from latex2sympy import process_sympy as pl

class Expression: 
    def __init__(self, string):
        self.string = string
        if '\\' in string: 
            self.string = self.tex_to_sympy(string)
    
    @classmethod
    def from_tex(cls, tex_string): 
        '''Given a Tex expression, return an Expression object'''
        return cls(cls.text_to_sympy(tex_string))
        
    @staticmethod
    def tex_to_sympy(tex_string): 
        return pl(tex_string)
    
    @classmethod
    def exprns_from_file(cls, file): 
        '''Given a Tex file, return an array of Expression objects for the expressions in the file.'''
        
        exprns = []
        # substrings matching this pattern are Tex math expressions
        exprn_pattern = re.compile(r'\\\(.*\\\)')
        start = re.compile(r'\\\(')
        end = re.compile(r'=?\s?\\\)')
        # sympy cannot parse ddfrac, so replace it with frac
        ddfrac = re.compile('d?dfrac')
        with open(file, 'r') as file: 
            tex_text = file.read()
            for item in exprn_pattern.findall(tex_text): 
                item = start.sub('', item)
                item = end.sub('', item)
                item = ddfrac.sub('frac', item)
                exprns.append(cls(item))
        return exprns
        
    def __repr__(self): 
        return str(self.string)
        
    def reduce(self):
        return sympy.Rational(sympy.simplify(self.string))

    
if __name__ == '__main__': 
    # These work.  Don't know why they need a "\\" to start, while below expressions only need "\frac..."
    # ex = Expression("\\frac{d}{dx} x^{2}")
    # ex = Expression("\\frac{256}{512}")
    # print(ex.reduce())
    
    filename = 'sample.txt'
    # if sys.argv[1]: 
        # filename = sys.argv[1]
        # print(type(filename))
        # print(filename)

    for item in Expression.exprns_from_file(filename):
        simplified = ''
        if not re.search('[a-zA-Z]', str(item)): 
            # If there are no variables in the expression, reduce it
            simplified = str(item.reduce())
        print(str(item) + ' = ' + simplified)
   
# A simpler Tex test string than the entire file   
test_exprns = '''\item \(\ddfrac{3}{4} * \ddfrac{1}{2} = \) \vspace{4em}
    \item \(\ddfrac{5}{7} * \ddfrac{1}{5} = \) \vspace{4em}'''