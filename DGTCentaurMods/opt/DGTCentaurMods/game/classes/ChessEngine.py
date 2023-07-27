# Play any uci engine without DGT Centaur Adaptive Play
#
# This file is part of the DGTCentaur Mods open source software
# ( https://github.com/EdNekebno/DGTCentaur )
#
# DGTCentaur Mods is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# DGTCentaur Mods is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see
#
# https://github.com/EdNekebno/DGTCentaur/blob/master/LICENSE.md
#
# This and any other notices must remain intact and unaltered in any
# distribution, modification, variant, or derivative of this software.

from DGTCentaurMods.game.classes import Log

import time
import chess
import chess.engine

# Wrapper intercepts inner engine exceptions that could occur...
class _ChessEngine():

    __engine = None
    __engine_options = None
    
    def __init__(self, engine_path):

        assert engine_path != None, "Need an engine_path!"

        self.__engine_path = engine_path

    def __instanciate(self):

        try:
            self.__engine = None
            self.__engine = chess.engine.SimpleEngine.popen_uci(self.__engine_path)
            
            Log.debug(f'_ChessEngine.__instanciate({id(self.__engine)})')
            
            if self.__engine_options != None:
                self.__engine.configure(self.__engine_options)

        except Exception as e:
            Log.exception(f"_ChessEngine.__instanciate error:{e}")
            self.__engine = None
            pass

    def __process(self, function_invoker):

        # 3 retries
        for _ in range(1,3):

            result = function_invoker()

            if result != None:
                return result
            
            # Failure...
            # We try anyway to quit the current engine...
            try:
                self.__engine.quit()
            except:
                pass

            # Another try with a FRESH engine!
            self.__engine == None

            time.sleep(.5)

    def configure(self, engine_options = None):

        self.__engine_options = engine_options

    def analyse(self, board, limit):

        def _analyse(board, limit):
            try:
                if self.__engine == None:
                    self.__instanciate()

                if self.__engine != None:
                    return self.__engine.analyse(board=board, limit=limit)

            except Exception as e:
                Log.exception(f"_ChessEngine.analyse error:{e}")
                pass

            return None
        
        return self.__process(lambda:_analyse(board=board, limit=limit))

    def play(self, board, limit, info):

        def _play(board, limit, info):
            try:
                if self.__engine == None:
                    self.__instanciate()

                if self.__engine != None:
                    return self.__engine.play(board=board, limit=limit, info=info)

            except Exception as e:
                Log.exception(f"_ChessEngine.play error:{e}")
                pass

            return None
        
        return self.__process(lambda:_play(board=board, limit=limit, info=info))

    def quit(self):

        try:
            if self.__engine != None:

                Log.debug(f'_ChessEngine.quit({id(self.__engine)})')

                self.__engine.quit()

        except Exception as e:
            Log.exception(f"_ChessEngine.quit error:{e}")
            pass

def get(uci_path):
    return _ChessEngine(uci_path)