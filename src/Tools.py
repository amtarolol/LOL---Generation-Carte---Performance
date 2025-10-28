import math

class Tools:
    
    @staticmethod
    def get_distance_line_point(line_begin_pos, line_end_pos, point_pos):

        line_begin_x = line_begin_pos[0]
        line_begin_y = line_begin_pos[1]

        line_end_x = line_end_pos[0]
        line_end_y = line_end_pos[1]

        point_x = point_pos[0]
        point_y = point_pos[1]

        # A = line_point_begin
        # B = line_point_end
        # (x,y) = point x,y
        # |(By​−Ay​)⋅x−(Bx​−Ax​)⋅y+Bx​⋅Ay​−By​⋅Ax​∣
        # sqrt((By​−Ay​)2+(Bx​−Ax​)2)
        dividende = math.fabs((line_end_y - line_begin_y) * point_x - 
                             (line_end_x - line_begin_x) * point_y + 
                             line_end_x * line_begin_y - line_end_y * line_begin_x)
        diviseur = math.sqrt((line_end_y - line_begin_y)**2 + (line_end_x - line_begin_x)**2)

        return dividende / diviseur


