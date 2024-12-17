
if __name__=="__main__":
    title = ["junior", "middle", "senior", "principle", 
             "senior principle", "chief expert", "distiguished expert", "CTO"]
    salary = [5, 10, 20, 30, 50, 80, 120, 200]
    print("Hello, Software Engineers!")
    for level in title:
        print("%s, salary: %d" % (level, salary[title.index(level)]))
