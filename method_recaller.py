from tracemalloc import start


i,f,s,l,d,t = int(),float(),str(),list(),dict(),tuple()
methodz = (i,f,s,l,d,t)

startup_message = ".....program starts here....."
formatted_message = " ".join(list(startup_message.upper()))
print(f"\n\n{formatted_message}\n\n")

for dtype in methodz:
    print(f"methods for type({type(dtype)})")
    print([x for x in dir(dtype) if not x.startswith('__')])
    print()