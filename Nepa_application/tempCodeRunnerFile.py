
def containsDuplicate(nums):
    unique_elements = set()
    # print(unique_elements)
    for num in nums:
        print(unique_elements)
        if num in unique_elements:
            return True
        else:
            unique_elements.add(num)
    return False

nums = [1,2,3,4,5,6,7,8,1,9,10,11,12,13,14,15,1]
print(containsDuplicate(nums))