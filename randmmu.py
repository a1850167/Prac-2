from mmu import MMU
import sys

import random

class RandMMU(MMU):
    def __init__(self, frames):
        # TODO: Constructor logic for RandMMU
        self.frames = frames
        self.ref_bit = [0] * frames # 1 = recently used, 0 = cleared and increment clock
        self.dirty_bit = [0] * frames # dirty page/bit indicator
        
        self.indexes = {} # Stores pages in a set
        self.memory = [-1] * frames # Memory array is empty 
                
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

    def replace_and_update(self, page_number):
        self.page_faults += 1
        
        # If memory or array is empty, 
        if -1 in self.memory: 
            empty_frame = self.memory.index(-1)
            self.memory[empty_frame] = page_number
            self.ref_bit[empty_frame] = 1
            self.dirty_bit[empty_frame] = 0
            self.indexes[page_number] = empty_frame
            self.disk_reads += 1
        else:
            random_page = random.randint(0, len(self.ref_bit) - 1)
            
            if self.dirty_bit[random_page] == 1:
                self.disk_writes += 1
                
            self.memory[random_page] = page_number
            self.ref_bit[random_page] = 1
            self.dirty_bit[random_page] = 0 
            self.disk_reads += 1

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
