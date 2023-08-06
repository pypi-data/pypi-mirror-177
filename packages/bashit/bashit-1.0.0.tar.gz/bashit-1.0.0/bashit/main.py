def main(argv=None):
    import sys, os, tempfile
    with tempfile.NamedTemporaryFile("x+") as f:
        with open(f.name, "w") as ff:
            ff.write(' '.join(sys.argv[1:]) + '\n')
        os.system(f"bash {f.name}")
      
    
if __name__ == "__main__":
    main()
