start = 1000
end = 10000

print(sum([int(d) for d in str(start)]))

counter = 0
for index, i in enumerate(range(start, end)):
    list_nums = [int(d) for d in str(i)]
    if i % 2 == 0 and i % 10 == 0 and sum(list_nums) == 9 and ((list_nums[2] * 10 + list_nums[3]) % 4 == 0) and i % 7 == 0:
        print(counter, i)
        counter += 1