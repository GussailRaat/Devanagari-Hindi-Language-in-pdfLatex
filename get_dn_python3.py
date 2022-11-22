# python3 compatible
# python devnagri_latex.py dn file.txt
import os
import re
import subprocess
import sys

consonants = {
	0x0915: ['k'],
	0x0916: ['kh'],
	0x0917: ['g'],
	0x0918: ['gh'],
	0x0919: ['"n'],
	0x091A: ['c'],
	0x091B: ['ch'],
	0x091C: ['j'],
	0x091D: ['jh'],
	0x091E: ['~n'],
	0x091F: ['.t'],
	0x0920: ['.th'],
	0x0921: ['.d'],
	0x0922: ['.dh'],
	0x0923: ['.n'],
	0x0924: ['t'],
	0x0925: ['th'],
	0x0926: ['d'],
	0x0927: ['dh'],
	0x0928: ['n'],
	0x092A: ['p'],
	0x092B: ['ph'],
	0x092C: ['b'],
	0x092D: ['bh'],
	0x092E: ['m'],
	0x092F: ['y'],
	0x0930: ['r'],
	0x0932: ['l'],
	0x0933: ['L'],
	0x0935: ['v'],
	0x0936: ['"s'],
	0x0937: ['.s'],
	0x0938: ['s'],
	0x0939: ['h'],
	0x0958: ['q'],
	0x0959: ['.kh'],
	0x095A: ['.g'],
	0x095B: ['z'],
	0x095C: ['R'],
	0x095D: ['Rh'],
	0x095E: ['f'],
}
vowel_signs = {
	0x093E: ['aa'],
	0x093F: ['i'],
	0x0940: ['ii'],
	0x0941: ['u'],
	0x0942: ['uu'],
	0x0943: ['.r'],
	0x0944: ['.R', '.r.r'],
	0x0947: ['e'],
	0x0948: ['ai'],
	0x0949: ['~o'],
	0x094B: ['o'],
	0x094C: ['au'],
	0x0962: ['.l'],
	0x0963: ['.ll', '.l.l'],
}
vowels = {
	0x0905: ['a'],
	0x0906: ['aa'],
	0x0907: ['i'],
	0x0908: ['ii'],
	0x0909: ['u'],
	0x090A: ['uu'],
	0x090B: ['.r'],
	0x090C: ['.l'],
	0x090F: ['e'],
	0x0910: ['ai'],
	0x0913: ['o'],
	0x0914: ['au'],
	0x0960: ['.R'],
	0x0961: ['.L'],
	0x0972: ['~a'],
}
other = {
	# 0x002E: ['..'],
	0x0901: ['/'],
	0x0902: ['.m'],
	0x0903: ['.h'],
	0x093D: ['.a'],
	0x094D: ['&'],
	0x0950: ['.o'],
	0x0964: ['|'],
	0x0965: ['||'],
	0x0966: ['0'],
	0x0967: ['1'],
	0x0968: ['2'],
	0x0969: ['3'],
	0x096A: ['4'],
	0x096B: ['5'],
	0x096C: ['6'],
	0x096D: ['7'],
	0x096E: ['8'],
	0x096F: ['9'],
	0x0970: ['@'],
	0x0971: ['#'],
}


ITRANS = {
	'अ':"a",
	'आ':"A",
	'इ':"i",
	'ई':"I",
	'उ':"u",
	'ऊ':"U",
	'ए':"E",
	'ऎ':"e",
	'ऐ':"ai",
	'ा':"A",
	'ि':"i",
	'ी':"I",
	'ु':"u",
	'ू':"U",
	'े':"E",
	'ै':"ai",
	'ऒ':"o",
	'ओ':"O",
	'औ':"au",
	'ो':"O",
	'ौ':"au",
	'ऋ':"RRi",
	'ॠ':"RRI",
	'ऌ':"LLi",
	'ॡ':"LLI",
	'अं':"M",
	'ं':"M",
	'अः':"H",
	'ः':"H",
	'अँ':".N",
	'ाँ':".N",
	'ऽ':".a",
	'क':"ka",
	'ख':"kha",
	'ग':"ga",
	'घ':"gha",
	'ङ':"~Na",
	'च':"cha",
	'छ':"Chha",
	'ज':"ja",
	'झ':"jha",
	'ञ':"~na",
	'ट':"Ta",
	'ठ':"Tha",
	'ड':"Da",
	'ढ':"Dha",
	'ण':"Na",
	'त':"ta",
	'थ':"tha",
	'द':"da",
	'ध':"dha",
	'न':"na",
	'प':"pa",
	'फ':"pha",
	'ब':"ba",
	'भ':"bha",
	'म':"ma",
	'य':"ya",
	'र':"ra",
	'ल':"la",
	'व':"va",
	'श':"sha",
	'ष':"Sha",
	'स':"sa",
	'ह':"ha",
	'क्ष':"kSha",
	'त्र':"tra",
	'ज्ञ':"GYa",
	'श्र':"shra",
	'क़':"qa",
	'ख़':"Ka",
	'ग़':"Ga",
	'ज़':"za",
	'फ़':"fa",
	'ड़':".Da",
	'ढ़':".Dha",
	'ऴ':"zha",
	'ऱ':"Ra",
	'ऩ':"^na",
	# ------- not included in the official mapping, but I had to include it
	'्':""
}

re_consonant = '|'.join(chr(n) for n in consonants)
re_vowel_sign = '|'.join(chr(n) for n in vowel_signs)
re_vowel = '|'.join(chr(n) for n in vowels)
re_other = '|'.join(chr(n) for n in other)
re_virama = chr(0x094D)
re_a = vowels[0x0905][0]  # 'a'

def velthuis(devanagari):
	text = devanagari
	text = re.sub('(%s)(%s)' % (re_consonant, re_vowel_sign),
				  lambda match: consonants[ord(match.group(1))][0] + vowel_signs[ord(match.group(2))][0],
				  text)
	text = re.sub('(%s)(%s)' % (re_consonant, re_virama),
				  lambda match: consonants[ord(match.group(1))][0],
				  text)
	text = re.sub('(%s)' % re_consonant,
				  lambda match: consonants[ord(match.group(1))][0] + re_a,
				  text)
	text = re.sub('(%s)' % re_vowel,
				  lambda match: vowels[ord(match.group(1))][0],
				  text)
	text = re.sub('(%s)' % re_other,
				  lambda match: other[ord(match.group(1))][0],
				  text)
	return text

def wikner(devanagari):
	text = devanagari
	text = re.sub('(%s)(%s)' % (re_consonant, re_vowel_sign),
				  lambda match: consonants[ord(match.group(1))][-1] + vowel_signs[ord(match.group(2))][-1],
				  text)
	text = re.sub('(%s)(%s)' % (re_consonant, re_virama),
				  lambda match: consonants[ord(match.group(1))][-1],
				  text)
	text = re.sub('(%s)' % re_consonant,
				  lambda match: consonants[ord(match.group(1))][-1] + re_a,
				  text)
	text = re.sub('(%s)' % re_vowel,
				  lambda match: vowels[ord(match.group(1))][-1],
				  text)
	text = re.sub('(%s)' % re_other,
				  lambda match: other[ord(match.group(1))][-1],
				  text)
	return text


random_filename = 'lwfzal3XBeV8H10I8f4n'

nukta_dict = {
		#combination : unicode
		'क़': 'क़',
		'ख़': 'ख़',
		'ग़': 'ग़',
		'ज़': 'ज़',
		'ड़': 'ड़',
		'ढ़': 'ढ़',
		'फ़': 'फ़',
		'य़': 'य़',
		'ऱ': 'ऱ',
		'ऴ': 'ऴ',
		'ऩ': 'ऩ',
	}
# Use this to see unicode numbers in a string 'abc'
# ['U+%04X' % (ord(ch)) for ch in 'abc']

def get_preprocessed(text, ext):
	preprocessor = {
		'dn': 'devnag',
		'skt': './skt',
	}
	assert ext in preprocessor.keys(), ext
	for k in nukta_dict.keys():
		text = text.replace(k,nukta_dict[k])
	transliterated = velthuis(text) if ext == 'dn' else wikner(text)
	infile = '%s-%s.%s' % (random_filename, ext, ext)
	open(infile, 'w').write(r'{\%s %s}' % (ext, transliterated))
	p = subprocess.Popen([preprocessor[ext], infile],
						 stdout=subprocess.PIPE,
						 stderr=subprocess.PIPE,
						 # shell=True,
						 close_fds=True)

	out, err, ret = p.stdout.read(), p.stderr.read(), p.returncode
	if err or ret:
		print('input: <%s>' % text.encode('utf-8'))
		print('transliterated: <%s>' % transliterated)
		print('stdout: <%s>' % out)
		print('stderr: <%s>' % err)
		print('returned: <%s>' % ret)
		raise ValueError

	outfile = '%s-%s.tex' % (random_filename, ext)
	translation = open(outfile).read()
	os.remove(outfile)
	os.remove(infile)
	prefix = r'\def\DevnagVersion{2.17}{\dn ' if ext == 'dn' else r'{\skt '
	assert translation.startswith(prefix), translation
	assert translation.endswith('}')
	translation = translation[len(prefix):-1]
	return translation

if __name__ == '__main__':
    ext = sys.argv[1]
    filename = sys.argv[2]

    file_data = open(filename).read()
    # print(file_data)

    try:
        os.remove("dn_results.devnagout")
    except:
        pass

    for text in file_data.split('\n'):
        if len(text) != 0:
            out = get_preprocessed(text, ext)
            open('dn_results.devnagout', 'a').write('{\dn '+ out + '}\n' )
            # open('dn_results.devnagout', 'a').write(r'{\%s %s}' % (ext, out+'\n'))
