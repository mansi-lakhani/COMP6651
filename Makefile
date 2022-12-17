TARGET = 40197791_detector.py

FILE1 =
FILE2 =

all: $(TARGET)

run: $(TARGET)
	@python3 ./$(TARGET) $(FILE1) $(FILE2)

clean:
	$(RM) $(TARGET)

testPlagiarism: $(TARGET)
	@echo "Testing plagiarism test cases in ../data/plagiarismXX"
	@for file in ../data/plagiarism*; do echo "Testing $$file"; python3 ./$(TARGET) $$file/1.txt $$file/2.txt;done

testNonPlagiarism: $(TARGET)
	@echo "Testing non-plagiarism test cases in ../data/okayXX"
	@for file in ../data/okay*; do echo "Testing $$file"; python3 ./$(TARGET) $$file/1.txt $$file/2.txt;done

test: testPlagiarism testNonPlagiarism
