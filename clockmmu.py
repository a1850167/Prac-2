from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU
        self.frames = frames
        self.ref_bit = 0 # 1 = recently used, 0 = cleared and increment clock
        
        self.indexes = {} # Stores pages in a set        
        self.clock_hand = 0
        
        self.page_faults = 0
        self.disk_reads = 0
        self.disk_writes = 0
        pass

    def set_debug(self):
        # TODO: Implement the method to set debug mode
        self.debut = True
        pass

    def reset_debug(self):
        # TODO: Implement the method to reset debug mode
        self.debug = False
        pass

    def replace_and_update(self, page_number):
        self.page_faults += 1
        self.ref_bit[page_number] = 1 # page is moved to the back of queue and search continues
        self.indexes[page_number] = False # mark page as dirty
        self.indexes[page_number]
        self.disk_reads += 1
        
        # TODO: If reference bit is 0, page has not been recently used
        # TODO: If reference bit is 1, page has been recently used
        # https://www.geeksforgeeks.org/operating-systems/second-chance-or-clock-page-replacement-policy/

    
    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if page_number in self.indexes:
            frame_index = self.indexes[page_number]
            self.ref_bit[frame_index] = 1
        else:
            self.replace_and_update(page_number)
        pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if page_number in self.indexes:
            frame_index = self.indexes[page_number]
            self.ref_bit[frame_index] = 1
            self.indexes[frame_index] = True # mark page as dirty
        else: 
            self.replace_and_update(page_number)
            frame = self.indexes[page_number]
            self.indexes[page_number] = True # mark page as dirty
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
