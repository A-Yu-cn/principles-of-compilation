s = "   \t \n this is  a  and what happen"
print(s)
i = 0
while s[i] ==' ' or s[i]=='\n' or s[i]=='\t':
    i+=1
s = s[i:-1]
print(s)