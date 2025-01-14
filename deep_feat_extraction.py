import torch.nn as nn
import torch.nn.functional as F
from pointnet2_utils import PointNetSetAbstraction

class feat_extraction_layer(nn.Module):
    def __init__(self, use_normal = True):
        super(feat_extraction_layer, self).__init__()
        in_channel = 6 if use_normal else 3
        self.use_normal = use_normal
        self.sa1 = PointNetSetAbstraction(npoint = 10000, radius = 0.1, nsample = 256, in_channel = in_channel, mlp = [16, 16, 32], group_all = False)
        self.sa2 = PointNetSetAbstraction(npoint=10000, radius=0.2, nsample=128, in_channel = in_channel, mlp=[32, 64],
                                          group_all=False)
        self.sa3 = PointNetSetAbstraction(npoint=10000, radius=0.4, nsample=64, in_channel=in_channel, mlp=[64, 32],
                                          group_all=False)
        #self.fc = nn.Linear(64, 32)
        # self.sa2 = PointNetSetAbstraction(npoint = 10000, radius = 0.1, nsample = 8, in_channel = in_channel, mlp = [16, 16, 32], group_all = False)

    def forward(self, pts):
        B, _, _, = pts.shape
        if self.use_normal:
            normal = pts[:, 3:, :]
            xyz = pts[:, :3, :]
        else:
            normal = None
            xyz = pts
        output_xyz, output_pts = self.sa1(xyz, normal)
        output_xyz, output_pts = self.sa2(output_xyz, normal)
        output_xyz, output_pts = self.sa3(output_xyz, normal)
        output_xyz = output_xyz.permute(0, 2, 1)
        output_pts = output_pts.permute(0, 2, 1)

        return output_xyz, output_pts
