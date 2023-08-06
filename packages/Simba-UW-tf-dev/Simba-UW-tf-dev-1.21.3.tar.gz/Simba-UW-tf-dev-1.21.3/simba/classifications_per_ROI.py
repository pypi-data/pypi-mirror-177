__author__ = "Simon Nilsson", "JJ Choong"

import glob, os
from simba.rw_dfs import read_df
import numpy as np
from shapely import geometry
from shapely.geometry import Point
from simba.features_scripts.unit_tests import *
from datetime import datetime
from simba.read_config_unit_tests import read_config_file, read_config_entry
from simba.features_scripts.unit_tests import read_video_info_csv, read_video_info


class clf_within_ROI(object):
    """
    Class for computing aggregate statistics of classification results within user-defined ROIs.
    results are stored in `project_folder/logs` directory of the SimBA project.

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format

    Notes
    -----

    Examples
    -----
    >>> clf_ROI_analyzer = clf_within_ROI(config_ini="MyConfigPath")
    >>> clf_ROI_analyzer.perform_ROI_clf_analysis()
    """

    def __init__(self,
                 config_ini: str):

        self.config = read_config_file(ini_path=config_ini)
        self.projectPath = read_config_entry(self.config, 'General settings', 'project_path', data_type='folder_path')
        model_nos = read_config_entry(config=self.config, section='SML settings', option='No_targets', data_type='int')
        self.logFolderPath = os.path.join(self.projectPath, 'logs')
        self.video_info_df = read_video_info_csv(os.path.join(self.logFolderPath, 'video_info.csv'))
        self.body_parts_path = os.path.join(os.path.join(self.logFolderPath, 'measures', 'pose_configs', 'bp_names', 'project_bp_names.csv'))
        body_parts_df = pd.read_csv(self.body_parts_path, names=['bodyparts'])
        self.body_part_list = list(body_parts_df['bodyparts'])
        self.ROIcoordinatesPath = os.path.join(self.logFolderPath, 'measures', 'ROI_definitions.h5')
        if not os.path.isfile(self.ROIcoordinatesPath):
            print('No ROI coordinates found. Please use the [ROI] tab to define ROIs')
            raise FileNotFoundError()
        self.rectanglesInfo = pd.read_hdf(self.ROIcoordinatesPath, key='rectangles')
        self.circleInfo = pd.read_hdf(self.ROIcoordinatesPath, key='circleDf')
        self.polygonInfo = pd.read_hdf(self.ROIcoordinatesPath, key='polygons')

        self.ROI_str_name_list = []
        for index, row in self.rectanglesInfo.iterrows(): self.ROI_str_name_list.append(row['Shape_type'] + ': ' + row['Name'])
        for index, row in self.circleInfo.iterrows(): self.ROI_str_name_list.append(row['Shape_type'] + ': ' + row['Name'])
        for index, row in self.polygonInfo.iterrows(): self.ROI_str_name_list.append(row['Shape_type'] + ': ' + row['Name'])
        self.ROI_str_name_list = list(set(self.ROI_str_name_list))

        self.behavior_names = []
        for i in range(model_nos):
            self.behavior_names.append(self.config.get('SML settings', 'target_name_' + str(i + 1)))

    def perform_ROI_clf_analysis(self,
                                 ROI_dict_lists: dict,
                                 behavior_list: list,
                                 body_part_list: list):
        """
        Parameters
        ----------
        ROI_dict_lists: dict
            A dictionary with the shape type as keys (i.e., Rectangle, Circle, Polygon) and lists of shape names
            as values.
        behavior_list: list
            List of classifier names to calculate ROI statistics. E.g., ['Attack', 'Sniffing']
        body_part_list: list
            List of body-part names to use to infer animal location. Eg., ['Nose_1'].
        """

        machine_results_path = os.path.join(self.projectPath, 'csv', 'machine_results')
        wfileType = read_config_entry(config=self.config, section='General settings', option='workflow_file_type', data_type='str')
        files_found = glob.glob(machine_results_path + '/*.' + wfileType)
        if len(files_found) == 0:
            print('SIMBA ERROR: No machine learning results found in the project_folder/csv/machine_results directory. Create machine classifications before analyzing classifications by ROI')
            raise ValueError()
        print('Analyzing ' + str(len(files_found)) + ' files...')
        body_part_col_names = []
        body_part_col_names_x, body_part_col_names_y = [], []
        for body_part in body_part_list:
            body_part_col_names.extend((body_part + '_x', body_part + '_y', body_part + '_p'))
            body_part_col_names_x.append(body_part + '_x')
            body_part_col_names_y.append(body_part + '_y')
        all_columns = body_part_col_names + behavior_list

        self.frame_counter_dict = {}

        for file_path in files_found:
            current_df = read_df(file_path, wfileType,idx=0)
            self.video_name = Path(file_path).stem
            print('Analyzing ' + self.video_name + '...')
            shapes_in_video = len(self.rectanglesInfo.loc[(self.rectanglesInfo['Video'] == self.video_name)]) + len(self.circleInfo.loc[(self.circleInfo['Video'] == self.video_name)]) + len(self.polygonInfo.loc[(self.polygonInfo['Video'] == self.video_name)])
            if shapes_in_video == 0:
                print('WARNING: Video {} has 0 user-defined ROI shapes.'.format(self.video_name))
            currVideoSettings, currPixPerMM, self.fps = read_video_info(self.video_info_df, self.video_name)
            current_df = current_df[all_columns]
            for current_behavior in behavior_list:
                self.current_behavior = current_behavior
                current_behavior_df = current_df[body_part_col_names][current_df[current_behavior] == 1].reset_index(drop=True)
                for current_type in ROI_dict_lists:
                    self.current_type = current_type
                    for current_name in ROI_dict_lists[current_type]:
                        self.current_name = current_name
                        if current_type.lower() == 'rectangle':
                            current_rectangle_info = self.rectanglesInfo.loc[(self.rectanglesInfo['Video'] == self.video_name) & (self.rectanglesInfo['Shape_type'] == current_type) & (self.rectanglesInfo['Name'] == self.current_name)]
                            if len(current_rectangle_info) == 0:
                                pass
                            else:
                                topLeftX, topLeftY = current_rectangle_info['topLeftX'].values[0], current_rectangle_info['topLeftY'].values[0]
                                bottomRightX, bottomRightY = topLeftX + current_rectangle_info['width'].values[0], topLeftY + + current_rectangle_info['height'].values[0]
                                current_behavior_df['topLeftX'] = topLeftX
                                current_behavior_df['topLeftY'] = topLeftY
                                current_behavior_df['bottomRightX'] = bottomRightX
                                current_behavior_df['bottomRightY'] = bottomRightY
                                current_behavior_df.apply(lambda row: self.__inside_rectangle(row[body_part_col_names_x[0]], row[body_part_col_names_y[0]], row['topLeftX'], row['topLeftY'], row['bottomRightX'], row['bottomRightY']), axis=1)

                        if (current_type.lower() == 'circle') or (current_type.lower() == 'circledf'):
                            current_circle_info = self.circleInfo.loc[(self.circleInfo['Video'] == self.video_name) & ( self.circleInfo['Shape_type'] == current_type) & (self.circleInfo['Name'] == self.current_name)]
                            if len(current_circle_info) == 0:
                                pass
                            else:
                                centre_x, centre_y = current_circle_info['centerX'].values[0], current_circle_info['centerY'].values[0]
                                radius = current_circle_info['radius'].values[0]
                                current_behavior_df['centerX'] = centre_x
                                current_behavior_df['centerY'] = centre_y
                                current_behavior_df['radius'] = radius
                                current_behavior_df.apply(lambda row: self.__inside_circle(row[body_part_col_names_x[0]],
                                                                                            row[body_part_col_names_y[0]],
                                                                                            row['centerX'],
                                                                                            row['centerY'],
                                                                                            row['radius']), axis=1)
                        if current_type.lower() == 'polygon':
                            current_polygon_info = self.polygonInfo.loc[(self.polygonInfo['Video'] == self.video_name) & (self.polygonInfo['Shape_type'] == current_type) & (self.polygonInfo['Name'] == self.current_name)]
                            if len(current_polygon_info) == 0:
                                pass
                            else:
                                vertices = current_polygon_info['vertices'].values[0]
                                polygon_shape = []
                                for i in vertices:
                                    polygon_shape.append(geometry.Point(i))
                                current_behavior_df.apply(lambda row: self.__inside_polygon(row[body_part_col_names_x[0]], row[body_part_col_names_y[0]], polygon_shape), axis=1)

        self.__organize_output_data(self.frame_counter_dict)

    def __inside_rectangle(self, bp_x, bp_y, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
        self.__populate_dict()
        if (((top_left_x - 10) <= bp_x <= (bottom_right_x + 10)) and ((top_left_y - 10) <= bp_y <= (bottom_right_y + 10))):
            self.__add_to_counter()
        else:
            pass

    def __inside_circle(self, bp_x, bp_y, center_x, center_y, radius):
        self.__populate_dict()
        px_dist = int(np.sqrt((bp_x - center_x) ** 2 + (bp_y - center_y) ** 2))
        if px_dist <= radius:
            self.__add_to_counter()
        else:
            pass

    def __inside_polygon(self, bp_x, bp_y, vertices):
        self.__populate_dict()
        current_point = Point(int(bp_x), int(bp_y))
        current_polygon = geometry.Polygon([[p.x, p.y] for p in vertices])
        polygon_status = current_polygon.contains(current_point)
        if polygon_status:
            self.__add_to_counter()
        else:
            pass

    def __populate_dict(self):
        if not self.video_name in self.frame_counter_dict:
            self.frame_counter_dict[self.video_name] = {}
        if not self.current_name in self.frame_counter_dict[self.video_name]:
            self.frame_counter_dict[self.video_name][self.current_name] = {}
        if not self.current_behavior in self.frame_counter_dict[self.video_name][self.current_name]:
            self.frame_counter_dict[self.video_name][self.current_name][self.current_behavior] = 0

    def __add_to_counter(self):
        self.frame_counter_dict[self.video_name][self.current_name][self.current_behavior] += 1 / self.fps

    def __organize_output_data(self, frame_counter_dict):
        if len(frame_counter_dict.keys()) == 0:
            print('SIMBA ERROR: ZERO ROIs found the videos represented in the project_folder/csv/machine_results directory')
            raise ValueError('SIMBA ERROR: ZERO ROIs found the videos represented in the project_folder/csv/machine_results directory')
        out_df = pd.concat({k: pd.DataFrame(v) for k, v in frame_counter_dict.items()}, axis=1).T.reset_index()
        out_df = out_df.rename(columns={'level_0': 'Video', 'level_1': 'ROI'})
        out_df = out_df.fillna(0)
        time_columns = list(out_df.columns)
        time_columns.remove('Video')
        time_columns.remove('ROI')
        for column in time_columns:
            out_df = out_df.round({column: 3})
            out_df = out_df.rename(columns={column: str(column) + ' (s)'})
        dateTime = datetime.now().strftime('%Y%m%d%H%M%S')
        out_path = os.path.join(self.logFolderPath, 'Classification_time_by_ROI_' + str(dateTime) + '.csv')
        out_df.to_csv(out_path)
        print('All videos analysed.')
        print('Data saved @ ' + out_path)


# clf_ROI_analyzer = clf_within_ROI(config_ini="/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini")
# clf_ROI_analyzer.perform_ROI_clf_analysis()