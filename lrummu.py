from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for LruMMU
        self.frames = frames
        self.indexes = {} # Stores pages in a set
        self.page_frame = [] # Memory 
        self.page_faults = 0
        self.disk_reads = 0
        self.disk_writes = 0
        pass

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debug = True
        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False
        pass

    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        
        if page_number in self.page_frame: 
            self.page_frame.remove(page_number)
            self.page_frame.append(page_number)
        else: # Otherwise increment page fault and disk read
            self.page_faults += 1
            self.disk_reads += 1
        
            if len(self.page_frame) < self.frames:
                self.page_frame.append(page_number)
                self.indexes[page_number] = False # Dirty bit indicator
            else:
                # Removes first element off from frame list
                lru = self.page_frame.pop(0) 

                if self.indexes[lru]:
                    self.disk_writes += 1

                self.page_frame.append(page_number)
                self.indexes[page_number] = False 
        pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        
        # If page number is in the frame, remove from the frame and add it to the end
        # to indicate it has been recently used
        if page_number in self.page_frame:
            self.page_frame.remove(page_number)
            self.page_frame.append(page_number)
            self.indexes[page_number] = True # Marks new written page as dirty
        else:
            self.page_faults += 1
            self.disk_reads += 1

            # Checks if the frame can hold any pages
            # If frame has room, append/write new page to end of list
            if len(self.page_frame) < self.frames:
                self.page_frame.append(page_number)
                self.indexes[page_number] = True # Marks new written page as dirty
            else:
                # Removes first element off list as least recently used if frame is full
                lru = self.page_frame.pop(0)
                
                if self.indexes[lru]:
                    self.disk_writes += 1
                
                self.page_frame.append(page_number) # Add new page end of list
                self.indexes[page_number] = True # Marks new written page as dirty
        pass

    def get_total_disk_reads(self):
        # TODO: Implement the method to get total disk reads
        return self.disk_reads

    def get_total_disk_writes(self):
        # TODO: Implement the method to get total disk writes
        return self.disk_writes

    def get_total_page_faults(self):
        # TODO: Implement the method to get total page faults
        return self.page_faults
