from rclpy.node import Node
from sensor_msgs import Image
import numpy as np

class torchDepth_publisher(Node):

	
	def __init__(self, 	is_cuda = True):
		super().__init__('torch.minimal publisher')
		self.model = torch.load("model")
		self.device = 'cuda' if torch.cuda.is_avaliable() and is_cuda else 'cpu'
		self.model.to('device')
		self.get_logger().info(f"device selected is {self.device}")
		if self.device == 'cuda':
			self.get_logger().debug(f"model size  in gigabytes {torch.cuda.max_memory_allocated()}")
			
		self.create_publisher(Image, 'depthFromRGB', 10)
		self.image_stream = self.create_subscription(Image,'iamge_raw',self.depth_from_rgb)
		
		
		
		def depth_from_rgb(self,msg):
			pass
		
		
		
		
		
		
		
		