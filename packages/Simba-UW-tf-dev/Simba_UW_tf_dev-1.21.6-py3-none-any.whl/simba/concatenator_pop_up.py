from simba.read_config_unit_tests import read_config_file, read_config_entry
from tkinter import *
import os, glob
from simba.tkinter_functions import DropDownMenu
from simba.misc_tools import get_fn_ext, find_video_of_file
from frame_mergerer_ffmpeg import FrameMergererFFmpeg
import simba

class ConcatenatorPopUp(object):
    def __init__(self,
                 config_path: str):
        self.config, self.config_path = read_config_file(ini_path=config_path), config_path
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='folder_path')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.in_folder_path = os.path.join(self.project_path, 'csv', 'input_csv')
        self.icons_path = os.path.join(os.path.dirname(simba.__file__), 'assets', 'icons')
        self.icons_path = '/Users/simon/Desktop/simbapypi_dev/simba/assets/icons'
        self.videos_lst = []
        for file_path in glob.glob(self.in_folder_path +'/*.' + self.file_type):
            _, name, _ = get_fn_ext(filepath=file_path)
            self.videos_lst.append(name)
        self.main_frm = Toplevel()
        self.main_frm.minsize(500, 800)
        self.main_frm.wm_title('MERGE (CONCATENATE) VIDEOS')
        self.settings_frm = LabelFrame(self.main_frm, text='SETTING (VIDEOS TO MERGE)', pady=5, padx=5, font=("Helvetica", 12, 'bold'), fg='black')
        self.joint_type_frm = LabelFrame(self.main_frm, text='JOIN TYPE', pady=5, padx=5, font=("Helvetica", 12, 'bold'), fg='black')
        self.select_video_frm = LabelFrame(self.main_frm, text='SELECT VIDEO', pady=5, padx=5, font=("Helvetica", 12, 'bold'), fg='black')
        self.classifications_sklearn_var = BooleanVar()
        self.gantt_var = BooleanVar()
        self.data_var = BooleanVar()
        self.distance_var = BooleanVar()
        self.probability_var = BooleanVar()
        self.heatmaps_clf_var = BooleanVar()
        self.heatmaps_loc_var = BooleanVar()
        self.path_var = BooleanVar()
        self.classifications_sklearn_cb = Checkbutton(self.settings_frm, text='Classifications (sklearn)', variable=self.classifications_sklearn_var)
        self.gantt_cb = Checkbutton(self.settings_frm, text='Gantt plots', variable=self.gantt_var)
        self.data_cb = Checkbutton(self.settings_frm, text='Data plots', variable=self.data_var)
        self.distance_cb = Checkbutton(self.settings_frm, text='Distance plots', variable=self.distance_var)
        self.probability_cb = Checkbutton(self.settings_frm, text='Probability plots', variable=self.probability_var)
        self.heatmaps_clf_cb = Checkbutton(self.settings_frm, text='Heatmap (classifications)', variable=self.heatmaps_clf_var)
        self.heatmaps_loc_cb = Checkbutton(self.settings_frm, text='Heatmap (location)',variable=self.heatmaps_loc_var)
        self.path_cb = Checkbutton(self.settings_frm, text='Path plots', variable=self.path_var)
        self.resolution_width = DropDownMenu(self.settings_frm, 'Resolution width', ['480', '640', '1280', '1920', '2560'], '15')
        self.resolution_height = DropDownMenu(self.settings_frm, 'Resolution height', ['480', '640', '1280', '1920', '2560'], '15')
        self.video_dropdown = DropDownMenu(self.select_video_frm, 'Video: ', self.videos_lst, '12')
        self.video_dropdown.setChoices(self.videos_lst[0])
        self.resolution_width.setChoices('640')
        self.resolution_height.setChoices('480')

        self.join_type_var = StringVar()
        self.joint_type_frm.grid(row=2, sticky=NW)
        self.icons_dict = {}
        for file_cnt, file_path in enumerate(glob.glob(self.icons_path + '/*')):
            _, file_name, _ = get_fn_ext(file_path)
            self.icons_dict[file_name] = {}
            self.icons_dict[file_name]['img'] = PhotoImage(file=file_path)
            self.icons_dict[file_name]['btn'] = Radiobutton(self.joint_type_frm, text=file_name, variable=self.join_type_var, value=file_name)
            self.icons_dict[file_name]['btn'].config(image=self.icons_dict[file_name]['img'])
            self.icons_dict[file_name]['btn'].image = self.icons_dict[file_name]['img']
            self.icons_dict[file_name]['btn'].grid(row=0, column=file_cnt, sticky=NW)
        self.join_type_var.set(value='Mosaic')


        run_btn = Button(self.main_frm, text='RUN', command=lambda: self.run())
        self.data_dirs = {'Classifications (sklearn)': os.path.join(self.project_path, 'frames', 'output', 'sklearn_results'),
                          'Gantt plots': os.path.join(self.project_path, 'frames', 'output', 'gantt_plots'),
                          'Distance plots': os.path.join(self.project_path, 'frames', 'output', 'line_plot'),
                          'Probability plots': os.path.join(self.project_path, 'frames', 'output', 'probability_plots'),
                          'Path plots': os.path.join(self.project_path, 'frames', 'output', 'path_plots'),
                          'Data plots': os.path.join(self.project_path, 'frames', 'output', 'live_data_table'),
                          'Heatmap (classifications)': os.path.join(self.project_path, 'frames', 'output', 'heatmaps_classifier_locations'),
                          'Heatmap (location)': os.path.join(self.project_path, 'frames', 'output', 'heatmaps_locations')}
        self.video_dropdown.grid(row=0, column=0, sticky=NW)
        self.classifications_sklearn_cb.grid(row=1, column=0, sticky=NW)
        self.gantt_cb.grid(row=2, column=0, sticky=NW)
        self.data_cb.grid(row=3, column=0, sticky=NW)
        self.distance_cb.grid(row=4, column=0, sticky=NW)
        self.probability_cb.grid(row=5, column=0, sticky=NW)
        self.heatmaps_loc_cb.grid(row=6, column=0, sticky=NW)
        self.heatmaps_clf_cb.grid(row=7, column=0, sticky=NW)
        self.path_cb.grid(row=8, column=0, sticky=NW)
        self.resolution_width.grid(row=9, column=0, sticky=NW)
        self.resolution_height.grid(row=10, column=0, sticky=NW)
        self.select_video_frm.grid(row=0, column=0, sticky=NW)
        self.settings_frm.grid(row=1, column=0, sticky=NW)
        run_btn.grid(row=3, column=0, sticky=NW)

    def run(self):
        frame_types, video_name = {}, self.video_dropdown.getChoices()
        for var, name in zip([self.classifications_sklearn_var, self.gantt_var, self.data_var, self.distance_var, self.probability_var, self.path_var, self.heatmaps_clf_var, self.heatmaps_loc_var], ['Classifications (sklearn)', 'Gantt plots', 'Data plots', 'Distance plots', 'Probability plots', 'Path plots', 'Heatmap (classifications)', 'Heatmap (location)']):
            if var.get():
                video_path = find_video_of_file(video_dir=self.data_dirs[name], filename=video_name)
                if video_path is None:
                    print('SIMBA ERROR: Could not locate a video representing {} inside the {} directory. Create this video before concatenating it to other videos.'.format(video_name, self.data_dirs[name]))
                    raise FileNotFoundError('SIMBA ERROR: Could not locate a video representing {} inside the {} directory. Create this video before concatenating it to other videos, or leave this video-type un-checked.'.format(video_name, self.data_dirs[name]))
                else:
                    frame_types[name] = video_path
        if len(frame_types.keys()) < 2:
            print('SIMBA ERROR: Please select at least two videos to merge/concatenate.')
            raise ValueError('SIMBA ERROR: Please select at least two videos to merge/concatenate.')

        if (len(frame_types.keys()) < 3) & (self.join_type_var.get() == 'mixed_mosaic'):
            print('SIMBA ERROR: if using the mixed mosaic join type, please tick check-boxes for at leasr three video types.')
            raise ValueError()

        _ = FrameMergererFFmpeg(config_path=self.config_path,
                                video_name=video_name,
                                frame_types=frame_types,
                                video_height=int(self.resolution_height.getChoices()),
                                video_width=int(self.resolution_width.getChoices()),
                                concat_type=self.join_type_var.get())

test = ConcatenatorPopUp(config_path='/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini')
test.main_frm.mainloop()
