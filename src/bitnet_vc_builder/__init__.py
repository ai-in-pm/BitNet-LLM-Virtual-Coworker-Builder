"""
BitNet Virtual Co-worker Builder - A framework for building AI virtual co-workers using BitNet's 1-bit quantized language models.
"""

from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker
from bitnet_vc_builder.models.bitnet_wrapper import BitNetModel
from bitnet_vc_builder.tools.base_tools import Tool
from bitnet_vc_builder.memory.memory import Memory
from bitnet_vc_builder.core.team import BitNetTeam

# For backward compatibility
from bitnet_vc_builder.core.virtual_coworker import BitNetVirtualCoworker as BitNetAgent

__version__ = "0.2.0"
