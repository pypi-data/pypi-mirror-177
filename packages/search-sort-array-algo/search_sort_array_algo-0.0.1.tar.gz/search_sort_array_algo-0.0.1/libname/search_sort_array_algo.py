class search_algo:
    """
    This Class is for Linear Search and Binary Search Algorithms.
    """
    def linearSearch(self,arr,target):
        """
        
        This is Linear Search Algorithm , which works in O(n).
        This Function RETURN THE INDEX OF THE TARGET.
        
        """
        for i in range(len(arr)):
            if arr[i] == target:
                return i
        return "NO SUCH VALUE IN THE LIST."
    
    def binarySearch(self,arr,target):
        l = 0
        r = len(arr)-1
        mid = (l+r)//2
        for i in range(len(arr)):
            if arr[i] == target:
                return i
            else:
                if target<arr[mid]:
                    l = mid
                else:
                    r = mid

        return "NO SUCH VALUE IN THE LIST."