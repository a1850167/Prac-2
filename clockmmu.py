from mmu import MMU

class ClockMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for EscMMU
        self.frames = frames
        self.ref_bit = [0] * frames # 1 = recently used, 0 = cleared and increment clock
        self.dirty_bit = [0] * frames # dirty page/bit indicator
        
        self.indexes = {} # Stores pages in a set
        self.memory = [-1] * frames # Memory array is empty 
        
        self.clock_hand = 0 # Clock starts at 0
        
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
        
        if -1 in self.memory: # If memory or array is empty, 
            empty_frame = self.memory.index(-1)
            self.memory[empty_frame] = page_number
            self.ref_bit[empty_frame] = 1
            self.dirty_bit[empty_frame] = 0
            self.indexes[page_number] = empty_frame
            self.disk_reads += 1
        else:
            while True:
                # If reference bit is 0, page has not been recently used
                if self.ref_bit[self.clock_hand] == 0:
                    pop_page = self.memory[self.clock_hand]

                    # If reference bit is 1, page has been recently used -> disk write
                    if self.dirty_bit[self.clock_hand] == 1:
                        self.disk_writes += 1

                    self.memory[self.clock_hand] = page_number
                    self.indexes.pop(pop_page)
                    self.indexes[page_number] = self.clock_hand
                    self.ref_bit[self.clock_hand] = 1
                    self.dirty_bit[self.clock_hand] = 0 
                    self.clock_hand = (self.clock_hand + 1) % self.frames # Increment clock to next page
                    self.disk_reads += 1
                    break
                else:
                    self.ref_bit[self.clock_hand] = 0
                    self.clock_hand = (self.clock_hand + 1) % self.frames # Increment clock to next page
    
    def read_memory(self, page_number):
        # TODO: Implement the method to read memory
        if page_number in self.indexes:
            page_frame = self.indexes[page_number]
            self.ref_bit[page_frame] = 1
        else:
            self.replace_and_update(page_number)
        pass

    def write_memory(self, page_number):
        # TODO: Implement the method to write memory
        if page_number in self.indexes:
            page_frame = self.indexes[page_number]
            self.ref_bit[page_frame] = 1
            self.dirty_bit[page_frame] = 1 # mark page as dirty
        else: 
            self.replace_and_update(page_number)
            page_frame = self.indexes[page_number]
            self.dirty_bit[page_frame] = 1 # mark page as dirty
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
