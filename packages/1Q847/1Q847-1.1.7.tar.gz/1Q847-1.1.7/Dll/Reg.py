import ctypes
import os
from subprocess import Popen, PIPE

from comtypes.client import CreateObject


class RegDm:

    @classmethod
    def reg(cls):
        path = os.path.dirname(__file__)
        reg_dm = ctypes.windll.LoadLibrary(path + r'\DmReg.dll')
        reg_dm.SetDllPathW(path + r'\dm.dll', 0)
        return CreateObject(r'dm.dmsoft')

    @classmethod
    def create_dm(cls):
        return CreateObject(r'dm.dmsoft')


class LDCmd:
    def __init__(self, path: str):
        os.putenv('Path', path)

    @staticmethod
    def read_message(cmd):
        res = Popen(cmd, stdout=PIPE, shell=True)
        res = res.stdout.read().decode(encoding='GBK')
        return res

    def lunch(self, order: str):
        self.read_message('ldconsole.exe launch --index ' + order)

    def quit(self, order: str):
        self.read_message(cmd='ldconsole.exe quit --index ' + order)

    def get_message(self):
        return self.read_message('ldconsole.exe  list2')
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID

    def add(self, name: str):
        self.read_message('ldconsole.exe add --name ' + name)

    def remove(self, order: str):
        self.read_message('ldconsole.exe remove --index ' + order)

    def copy(self, name: str, order: str):
        self.read_message('ldconsole.exe copy --name ' + name + ' --from ' + order)

    def start_app(self, order: str, packagename: str):
        self.read_message('ldconsole.exe runapp --index ' + order + ' --packagename ' + packagename)

    def close_app(self, order: str, packagename: str):
        self.read_message('ldconsole.exe killapp --index ' + order + ' --packagename ' + packagename)

    def get_list_package(self, order: str):
        return self.read_message(cmd='ld.exe -s ' + order + '  pm list packages')

    def install_app(self, order: str, path: str):
        self.read_message('ldconsole.exe  installapp --index ' + order + ' --filename ' + path)

    def sort_wnd(self):
        self.read_message('ldconsole.exe sortWnd')

    def reboot(self, order: str):
        self.read_message('ldconsole.exe reboot --index ' + order)

    def get_appoint_game_hwd(self, order: str):
        my_list = self.get_message()
        items = my_list.splitlines()
        return items[int(order)].split(',')[3]


class Memory:
    def __init__(self, dx, hwd):
        self.__dx = dx
        self.hwd = hwd

    def get_call_address(self, s, model, off):
        # 返回16进制字符串地址
        module_size = self.__dx.GetModuleSize(self.hwd, model)
        base_address = self.__dx.GetModuleBaseAddr(self.hwd, model)
        end_address = module_size + base_address
        call_address = self.__dx.FindData(self.hwd, hex(base_address)[2:] + '-' + hex(end_address)[2:], s)
        return hex(int(call_address, 16) + int(off, 16))[2:]

    def x64_get_base_address(self, s, model, off):
        address = self.get_call_address(s, model, off)
        address_2 = self.__dx.readint(self.hwd, address, 4)
        return hex(int(address, 16) + address_2 + 4)[2:]

    def x32_get_base_address(self, s, model, off):
        address = self.get_call_address(s, model, off)
        address = self.__dx.readint(self.hwd, address, 4)
        return hex(address)[2:]


if __name__ == '__main__':
    dm = RegDm.reg()
    m = Memory(dm, 264360)
    print(m.x64_get_base_address('49 8B DD 48 8B C3 48 8B 4D 17 48 33 CC', 'ElementClient_64.exe', '68'))
