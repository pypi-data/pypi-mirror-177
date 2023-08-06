import os
import re
import shutil
from kabaret import flow
from libreflow.baseflow.file import (
    TrackedFile            as BaseTrackedFile,
    TrackedFolder          as BaseTrackedFolder,
    Revision               as BaseRevision,
    TrackedFolderRevision  as BaseTrackedFolderRevision,
    FileSystemMap          as BaseFileSystemMap,
)
from libreflow.utils.os import remove_folder_content


class Revision(BaseRevision):
    pass


class TrackedFolderRevision(BaseTrackedFolderRevision):
    pass


class SessionChoiceValue(flow.values.SessionValue):
    
    DEFAULT_EDITOR = 'choice'
    STRICT_CHOICES = False

    def choices(self):
        raise NotImplementedError()

    def revert_to_default(self):
        choices = self.choices()

        if choices:
            self.set_watched(False)
            self.set(choices[0])
            self.set_watched(True)


class RevisionName(SessionChoiceValue):

    _file = flow.Parent(2)

    def choices(self):
        return self._file.get_revision_names(
            sync_status='Available',
            published_only=True
        )
    
    def revert_to_default(self):
        if self._file.is_empty():
            self.set('')
            return

        revision = self._file.get_head_revision(sync_status='Available')
        revision_name = ''
        
        if revision is None:
            choices = self.choices()
            if choices:
                revision_name = choices[0]
        else:
            revision_name = revision.name()
        
        self.set_watched(False)
        self.set(revision_name)
        self.set_watched(True)


class ShotType(SessionChoiceValue):

    def choices(self):
        return self.root().project().admin.project_settings.shot_types.get()


class ShotIndex(SessionChoiceValue):

    def choices(self):
        return self.root().project().admin.project_settings.shot_indexes.get()


class ShotVersion(SessionChoiceValue):

    def choices(self):
        return self.root().project().admin.project_settings.shot_versions.get()


class RenameImageSequence(flow.Action):

    title = flow.SessionParam('<h2>Rename image sequence</h2>').ui(editor='label', wrap=True).ui(editable=False, label='')
    revision = flow.SessionParam(None, RevisionName).watched()
    shot_type = flow.SessionParam(None, ShotType).watched()
    shot_index = flow.SessionParam(None, ShotIndex).watched()
    shot_version = flow.SessionParam(None, ShotVersion).watched()
    summary_ = flow.SessionParam('').ui(editor='label', wrap=True).ui(editable=False, label='')

    _folder = flow.Parent()
    _files = flow.Parent(2)
    _shot = flow.Parent(5)

    def __init__(self, parent, name):
        super(RenameImageSequence, self).__init__(parent, name)
        self._first_file = None

    def allow_context(self, context):
        return context and not self._folder.is_empty(on_current_site=True)
    
    def needs_dialog(self):
        self.revision.revert_to_default()
        self.shot_type.revert_to_default()
        self.shot_index.revert_to_default()
        self.shot_version.revert_to_default()
        self.message.revert_to_default()
        self.summary_.revert_to_default()
        
        files = self._get_file_sequence()

        if not files:
            self.message.set('The selected revision is empty.')
        elif self.shot_type.get() is None:
            self.message.set('You must define at least one shot type in the project settings.')
        elif self.shot_index.get() is None:
            self.message.set('You must define at least one shot index in the project settings.')
        elif self.shot_version.get() is None:
            self.message.set('You must define at least one shot version in the project settings.')
        else:
            self.summary_.set(
                f'Current name:\t{files[0]}\n\nNew name:\t{self._get_new_name(files[0])}'
            )
        
        return True
    
    def get_buttons(self):
        return ['Rename', 'Cancel']
    
    def child_value_changed(self, child_value):
        if child_value in (self.revision, self.shot_type, self.shot_index, self.shot_version):
            files = self._get_file_sequence()

            if not files:
                self.message.set('The selected revision is empty.')
                self.summary_.set('')
            else:
                self.message.set('')
                self.summary_.set(
                    f'Current name:\t{files[0]}\n\nNew name:\t{self._get_new_name(files[0])}'
                )
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        revision = self.revision.get()

        if revision is None:
            raise Exception('You are trying to run this action on an empty file !')
        
        new_prefix = self._get_new_prefix()

        if new_prefix is None:
            return self.get_result(close=False)
        
        src_dir = self._folder.get_revision(revision).get_path()
        dst_dir = self._ensure_folder_revision()

        for im in os.listdir(src_dir):
            new_im = self._get_new_name(im, new_prefix)
            shutil.copy2(os.path.join(src_dir, im), os.path.join(dst_dir, new_im))
            print(f'{os.path.join(src_dir, im)} -> {os.path.join(dst_dir, new_im)}')
    
    def _get_new_name(self, current_name, suffix=None):
        return f'{suffix or self._get_new_prefix() or ""}.{self._get_suffix(current_name)}'
    
    def _get_new_prefix(self):
        # m = re.search(r'\d+', self._shot.name())
        # shot_num = f'{int(m.group()):02}' if m else '<undefined>'
        # m = re.search(r'\d+', self.revision.get())
        # rev_num = f'V{int(m.group())}' if m else '<undefined>'
        params = (self.shot_type.get(), self.shot_index.get(), self.shot_version.get())
        if None in params:
            return None
        else:
            return '_'.join(params)
    
    def _get_suffix(self, current_name):
        try:
            return current_name.split('.', maxsplit=1)[1]
        except IndexError:
            return ''
    
    def _ensure_folder_revision(self):
        name = self._folder.name() + '_ok'
        
        if not self._files.has_folder(name):
            folder = self._files.add_folder(name, tracked=True)
            folder.file_type.set('Outputs')
        else:
            folder = self._files[name]
        
        rev = folder.get_revision(self.revision.get())

        if rev is None:
            rev = folder.add_revision(self.revision.get())

        path = rev.get_path()
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            remove_folder_content(path)
        
        return path
    
    def _get_file_sequence(self):
        folder = self._folder.get_revision(self.revision.get()).get_path()
        files = os.listdir(folder)
        files = [
            f for f in files
            if os.path.isfile(os.path.join(folder, f))
        ]
        return files


class TrackedFile(BaseTrackedFile):
    pass


class TrackedFolder(BaseTrackedFolder):
    
    rename_sequence = flow.Child(RenameImageSequence)
    # pass


class FileSystemMap(BaseFileSystemMap):
    pass
