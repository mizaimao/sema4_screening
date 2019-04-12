# sema4_screening
  
This is a repo created for sema4 screening test.
Python Version: 3.7.3, tested in macOS 10.14

## Files
```README.md``` This file.  
```Q1.py```, ```Q2.py``` and ```Q3.py``` corresponds to the scripts or programs written for Q1, Q2 and Q3, respectively.  
```mysqlHelper.py``` a helper script imported in Q1 and Q2 programs to reduce code redundancy.  
```requirements.txt``` additional package(s) that may be required to run these scripts.  

## Other Notes
1. Only the Q1 explicitly requires an output file, and therefore no files are written to disk for Q2 and Q3;  
2. Output of Q1 is both printed and saved to file. By default, file name is the name of gene;  
3. Header of output ```bed``` files are disabled in the script;  
4. Run Q1.py or Q2.py without any parameters will show demos;  
5. Q3 accepts either compressed format in ```.gz``` or ```.fa``` format; decompression was done on-the-fly using ```zcat``` without generating additional files. But its syntax may be different in macOS (testing environment) and Linux.
