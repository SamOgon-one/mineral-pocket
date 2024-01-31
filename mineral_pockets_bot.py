from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2, Point3


class MineralPocket(BotAI):

    def __init__(self):
        pass       

    async def on_start(self):

        await self.client.debug_show_map()
          
    async def on_step(self, iteration):

        if iteration == 1: # calculate once

            self.points_to_check = set([mineral.position + Point2((1.5, 0)) for mineral in self.mineral_field] + [mineral.position + Point2((-1.5, 0)) for mineral in self.mineral_field]) # left and right side of mineral
            self.pockets = [point for point in self.points_to_check if self.in_pathing_grid(point) and sum(self.in_pathing_grid(point+nei) for nei in [Point2((1, 0)), Point2((-1, 0)), Point2((0, 1)), Point2((0, -1))]) == 1] # pocket has only one pathable neighbor
            self.pockets_entrance = [pocket+point for pocket in self.pockets for point in [Point2((1, 0)), Point2((-1, 0)), Point2((0, 1)), Point2((0, -1))] if self.in_pathing_grid(pocket+point)] # that neighbor
            self.opposite_to_entrance = [pocket-point for pocket in self.pockets for point in [Point2((1, 0)), Point2((-1, 0)), Point2((0, 1)), Point2((0, -1))] if self.in_pathing_grid(pocket+point)] # middle step to find mineral
            self.minerals_with_pocket = [mineral for mineral in self.mineral_field for point in [Point2((0.5, 0)), Point2((-0.5, 0)), Point2((0, 0.5)), Point2((0, -0.5))] if mineral.position+point in self.opposite_to_entrance] # mineral center is shifted by .5

            print('Pocket position: ')
            [print(x, y) for x, y in sorted(self.pockets)]

            print('minerals_with_pocket position: ')
            [print(mineral.position) for mineral in self.minerals_with_pocket]

        if iteration > 1: # draw

            [self.client.debug_box2_out(pos=Point3((x, y, self.get_terrain_z_height(Point2((x, y)))-0.4)), half_vertex_length=0.45, color=Point3((0, 255, 0))) for x, y in self.pockets] # green
            [self.client.debug_box2_out(pos=Point3((x, y, self.get_terrain_z_height(Point2((x, y)))-0.4)), half_vertex_length=0.45, color=Point3((50, 200, 200))) for x, y in self.pockets_entrance] # dark
            # [self.client.debug_box2_out(pos=Point3((x, y, self.get_terrain_z_height(Point2((x, y)))-0.1)), half_vertex_length=0.45, color=Point3((255, 255, 255))) for x, y in self.opposite_to_entrance] # white
            [self.client.debug_box2_out(pos=mineral.position3d, half_vertex_length=0.45, color=Point3((255, 255, 50))) for mineral in self.minerals_with_pocket] # yellow


def main():
    run_game(
        maps.get("GlitteringAshesAIE"),
        [Bot(Race.Terran, MineralPocket(), name="mineral_pockets"),
         Computer(Race.Terran, Difficulty.Easy)],
     
        realtime=False,
        random_seed=0,
    )


if __name__ == "__main__":
    main()

# maps
# 2000AtmospheresAIE
# BerlingradAIE
# BlackburnAIE
# CuriousMindsAIE
# GlitteringAshesAIE
# HardwireAIE
