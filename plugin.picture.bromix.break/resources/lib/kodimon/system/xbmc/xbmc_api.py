import xbmcgui
import xbmcplugin

from ..info_labels import create_info_labels_from_item
from ...exceptions import KodimonException
from ...constants import *
from ...items import *
from ...abstract_provider import AbstractProvider


def run(provider):
    """

    :param provider:
    :return:
    """
    plugin = provider.get_plugin()

    results = None
    try:
        results = provider.navigate(plugin.get_path(), plugin.get_params())
    except KodimonException, ex:
        if provider.handle_exception(ex):
            provider.log(ex.message, LOG_ERROR)
            xbmcgui.Dialog().ok("Exception in ContentProvider", ex.__str__())
            pass
        return

    result = results[0]
    options = {}
    options.update(results[1])

    if isinstance(result, bool) and not result:
        xbmcplugin.endOfDirectory(plugin.get_handle(), succeeded=False)
    elif isinstance(result, VideoItem) or isinstance(result, AudioItem):
        _set_resolved_url(plugin, result)
    elif isinstance(result, DirectoryItem):
        _add_directory(plugin, result)
    elif isinstance(result, list):
        item_count = len(result)
        for item in result:
            if isinstance(item, DirectoryItem):
                _add_directory(plugin, item, item_count)
            elif isinstance(item, VideoItem):
                _add_video(plugin, item, item_count)
            elif isinstance(item, AudioItem):
                _add_audio(plugin, item, item_count)
            elif isinstance(item, ImageItem):
                _add_image(plugin, item, item_count)
            pass

        xbmcplugin.endOfDirectory(
            plugin.get_handle(), succeeded=True, cacheToDisc=options.get(AbstractProvider.RESULT_CACHE_TO_DISC, True))
        pass
    else:
        # handle exception
        pass

    provider.shut_down()
    pass


def _set_resolved_url(plugin, base_item, succeeded=True):
    list_item = xbmcgui.ListItem(path=base_item.get_uri())
    xbmcplugin.setResolvedUrl(plugin.get_handle(), succeeded=succeeded, listitem=list_item)

    """
    # just to be sure :)
    if not isLiveStream:
        tries = 100
        while tries>0:
            xbmc.sleep(50)
            if xbmc.Player().isPlaying() and xbmc.getCondVisibility("Player.Paused"):
                xbmc.Player().pause()
                break
            tries-=1
    """


def _add_directory(plugin, directory_item, item_count=0):
    item = xbmcgui.ListItem(label=directory_item.get_name(),
                            iconImage=u'DefaultFolder.png',
                            thumbnailImage=directory_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if directory_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', directory_item.get_fanart())
        pass
    if directory_item.get_context_menu() is not None:
        item.addContextMenuItems(directory_item.get_context_menu())
        pass

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=directory_item.get_uri(),
                                listitem=item,
                                isFolder=True,
                                totalItems=item_count)
    pass


def _add_video(plugin, video_item, item_count=0):
    item = xbmcgui.ListItem(label=video_item.get_name(),
                            iconImage=u'DefaultVideo.png',
                            thumbnailImage=video_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if video_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', video_item.get_fanart())
        pass
    if video_item.get_context_menu() is not None:
        item.addContextMenuItems(video_item.get_context_menu())
        pass

    item.setProperty(u'IsPlayable', u'true')

    item.setInfo(type=u'video', infoLabels=create_info_labels_from_item(video_item))

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=video_item.get_uri(),
                                listitem=item,
                                totalItems=item_count)
    pass


def _add_image(plugin, image_item, item_count):
    item = xbmcgui.ListItem(label=image_item.get_name(),
                            iconImage=u'DefaultPicture.png',
                            thumbnailImage=image_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if image_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', image_item.get_fanart())
        pass
    if image_item.get_context_menu() is not None:
        item.addContextMenuItems(image_item.get_context_menu())
        pass

    item.setInfo(type=u'picture', infoLabels=create_info_labels_from_item(image_item))

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=image_item.get_uri(),
                                listitem=item,
                                totalItems=item_count)
    pass


def _add_audio(plugin, audio_item, item_count):
    item = xbmcgui.ListItem(label=audio_item.get_name(),
                            iconImage=u'DefaultAudio.png',
                            thumbnailImage=audio_item.get_image())

    # only set fanart is enabled
    settings = plugin.get_settings()
    from ... import constants

    if audio_item.get_fanart() and settings.get_bool(constants.SETTING_SHOW_FANART, True):
        item.setProperty(u'fanart_image', audio_item.get_fanart())
        pass
    if audio_item.get_context_menu() is not None:
        item.addContextMenuItems(audio_item.get_context_menu())
        pass

    item.setProperty(u'IsPlayable', u'true')

    item.setInfo(type=u'music', infoLabels=create_info_labels_from_item(audio_item))

    xbmcplugin.addDirectoryItem(handle=plugin.get_handle(),
                                url=audio_item.get_uri(),
                                listitem=item,
                                totalItems=item_count)
    pass