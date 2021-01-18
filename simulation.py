import asyncio

class QueueSimulation:
    def __init__(self,number_of_servers,queuing_rate,processing_rate,
                max_cycles=50,print_time=1):
        self.number_of_servers = number_of_servers
        self._server_list = [0 for queue in range(number_of_servers)]  
        self.cycles = 0
        self.processed = 0
        self.max_cycles = max_cycles
        self.server_order = []
        
        self.queuing_rate = queuing_rate
        self.processing_rate = processing_rate
        self.print_time = print_time
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.simulation(loop))
        loop.close()
        
    async def simulation(self,loop):
        added_tasks = []
        added_tasks.append(loop.create_task(self.queue_up()))
        for server in range(self.number_of_servers):
            added_tasks.append(loop.create_task(self.process_at_index(server)))
        added_tasks.append(loop.create_task(self.async_print_lengths()))

        await asyncio.gather(*added_tasks)

    async def process_at_index(self,index):
        while (any(self.server_list) or not self.cycles):
            await asyncio.sleep(.01)
            while self.server_list[index]:
                await asyncio.sleep(self.processing_rate)
                self.server_list[index] -= 1
                # del self.server_list[index]
                self.processed += 1
        self.print_lengths()
        exit()
            
    def add_to_queue(self,min_index):
        self.server_list[min_index] += 1
        self.server_order.append(min_index)
        
    async def queue_up(self):
        while (any(self.server_list) or not self.cycles) and self.cycles != self.max_cycles:
            min_index = self.get_min_server()
            self.add_to_queue(min_index)
            self.cycles += 1
            await asyncio.sleep(self.queuing_rate)
        self.print_lengths()
        exit()
        
    def get_min_server(self):
        val,min_index = min([(q,i) for i,q in enumerate(self.server_list)])
        return min_index

    async def async_print_lengths(self):
        while (any(self.server_list) or not self.cycles):
            await asyncio.sleep(self.print_time)
            print('Cycles:',self.cycles)
            print(self.server_list)
            print('Processed:',self.processed)
            print('Total Currently Queued:',sum(self.server_list))
            print()
        exit()

    def print_lengths(self):
        print('Final Results')
        print('Cycles:',self.cycles)
        print(self.server_list)
        print('Processed:',self.processed)
        print('Total Currently Queued:',sum(self.server_list))

    @property
    def server_list(self):
        return self._server_list

    @server_list.setter
    def server_list(self,l):
        self._server_list = l
            
if __name__ == "__main__":
    QueueSimulation(5,1,2)
