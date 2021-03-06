# Built-ins
import inspect

# RO Modules
import roplus
import imgui

# In game modules
import data
import BigWorld
import gt

from pprint import pformat

class MainWindow(object):

    def __init__(self, botInstance):
        self.bot = botInstance
        self.visible = False
        self.attr_search = (0, '')
        self.debug_target_locked = False
        self.debug_all_targets = False
        self.debug_custom = False
        self.hide_methods = False
        roplus.registerCallback('ROPlus.OnDrawGUI', self.onDrawGuiCallback)

    def show(self):
        self.visible = True

    def onDrawGuiCallback(self, args):
        if self.visible:
            if imgui.begin('RODebug##debug_mainwindow', (300,350)):
                player = BigWorld.player()
                imgui.columns(2)
                imgui.separator()

                # Player Name
                imgui.text('Name')
                imgui.nextColumn()
                imgui.text(player.playerName if player else 'Not ingame')
                imgui.nextColumn()

                # Player health
                if hasattr(player, 'hp') and hasattr(player, 'mhp'):
                    imgui.text('Health')
                    imgui.nextColumn()
                    imgui.text('{0} / {1}'.format(player.hp, player.mhp))
                    imgui.nextColumn()

                # Player Mana
                if hasattr(player, 'mp') and hasattr(player, 'mmp'):
                    imgui.text('Mana')
                    imgui.nextColumn()
                    imgui.text('{0} / {1}'.format(player.mp, player.mmp))
                    imgui.nextColumn()

                # Player EXP
                if hasattr(player, 'exp') and hasattr(player, 'realLv'):
                    imgui.text('Experience')
                    imgui.nextColumn()
                    exp_label = '{0} / {1}'.format(player.exp, data.avatar_lv_data.data.get(player.realLv, {}).get('upExp', '?'))
                    imgui.text(exp_label)
                    imgui.nextColumn()

                # Players current position
                if hasattr(player, 'position'):
                    imgui.text('Position')
                    imgui.nextColumn()
                    imgui.text('{0}'.format(player.position))
                    # imgui.nextColumn()

                imgui.columns(1)

                # Targetting Sections
                imgui.separator()
                imgui.columns(2)

                if hasattr(player, 'targetLocked') and player.targetLocked:
                    target = player.targetLocked

                    # Draw some things about the target we have locked
                    imgui.text('targetLocked')
                    imgui.nextColumn()
                    imgui.text('{0} ({1})'.format(target.roleName, (target)))
                    imgui.nextColumn()

                    # target HP?
                    if hasattr(target, 'hp') and hasattr(target, 'mhp'):
                        imgui.text('Target Health')
                        imgui.nextColumn()
                        imgui.text('{0} / {1}'.format(target.hp, target.mhp))
                        imgui.nextColumn()

                    # target Mana
                    if hasattr(target, 'mp') and hasattr(target, 'mmp'):
                        imgui.text('Target Mana')
                        imgui.nextColumn()
                        imgui.text('{0} / {1}'.format(target.mp, target.mmp))
                        imgui.nextColumn()

                    # target Level
                    if hasattr(target, 'lv'):
                        imgui.text('Target Level')
                        imgui.nextColumn()
                        imgui.text('{0}'.format(target.lv))
                        imgui.nextColumn()

                    # target current position
                    if hasattr(target, 'position'):
                        imgui.text('Target Position')
                        imgui.nextColumn()
                        imgui.text('{0}'.format(target.position))
                        imgui.nextColumn()
                else:
                    imgui.text('No Target')

                imgui.columns(1)
                imgui.separator()
                if imgui.checkbox('Debug Target', self.debug_target_locked):
                    self.debug_target_locked = not self.debug_target_locked
                    self.debug_all_targets = False
                    self.debug_custom = False
                if imgui.checkbox('Debug All Targets (Super Fucking Slow!)', self.debug_all_targets):
                    self.debug_target_locked = False
                    self.debug_all_targets = not self.debug_all_targets
                    self.debug_custom = False
                if imgui.checkbox('Debug Custom', self.debug_custom):
                    self.debug_all_targets = False
                    self.debug_target_locked = False
                    self.debug_custom = not self.debug_custom
                if imgui.checkbox('Hide Methods', self.hide_methods):
                    self.hide_methods = not self.hide_methods

                imgui.text('Search Attributes: ')
                imgui.sameLine()
                self.attr_search = imgui.inputText('', '')

                # The real fun
                if self.debug_target_locked:
                    if hasattr(player, 'targetLocked'):
                        obj = [player.targetLocked]
                    else:
                        obj = None
                        self.debug_target_locked = False
                        imgui.text('No Target Locked.')
                elif self.debug_all_targets:
                    obj = BigWorld.entities.values()
                elif self.debug_custom:
                    # obj = [gt.gtDispatcher.dispatcher]
                    obj = BigWorld.entity(player.id)  #[player.cell]
                else:
                    obj = [player]  # vars(player).items()
                if obj:
                    IGNORED_ATTRS = ['__builtins__', '__dict__']
                    for o in obj:
                        if (self.debug_target_locked or self.debug_all_targets or self.debug_custom) and o == player:
                            imgui.text('Skipping: {0}'.format(o))
                            imgui.separator()
                            continue
                        imgui.text(str(o))
                        for item in dir(o):
                            if hasattr(o, item):
                                value = getattr(o, item)
                                search_conditions = [
                                    self.attr_search[1].lower() in item.lower(),
                                    self.attr_search[1].lower() in str(value).lower(),
                                ]
                                
                                if self.hide_methods:
                                    if callable(value):
                                        continue

                                if self.attr_search[0] and not any(search_conditions):
                                    continue
                                if True:  # not(inspect.ismethod(value) or inspect.isfunction(value)):
                                    if item and value and item not in IGNORED_ATTRS: # and not(item.startswith('__')):
                                        try:
                                            if isinstance(value, (dict, )):
                                                imgui.text('{0} = {1}'.format(item, pformat(value)).strip())
                                            else:
                                                imgui.text('{0} = {1}'.format(item, value).strip())
                                        except:
                                            imgui.text('{0} = {1}'.format(item, '(failed)'))
                        imgui.separator()
            imgui.end()