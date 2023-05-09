class Solution(object):
    def canPlaceFlowers(self, flowerbed, n):
        check_n = True if n >= 0 and n <= len(flowerbed) else False
        check_flowerbed = True if len(flowerbed) >= 1 and len(flowerbed) <= 10000 else False
        if check_n and check_flowerbed:
            sum = 0
            for z in range(0, len(flowerbed)):
                if not flowerbed[z]:
                    try:
                        ones_left = max(list(i for i in range((abs(z-2)+z-2)/2 ,z) if flowerbed[i] == 1))
                    except:
                        ones_left = -2
                    try:
                        ones_right = min(list(i for i in range(z,z+2) if flowerbed[i] == 1))
                    except:
                        ones_right = len(flowerbed)+2
                    if abs(ones_left - z) > 1 and abs(ones_right - z) > 1:
                        sum += 1
                        flowerbed[z] = 1
            if sum < n:
                return False
            else:
                return True