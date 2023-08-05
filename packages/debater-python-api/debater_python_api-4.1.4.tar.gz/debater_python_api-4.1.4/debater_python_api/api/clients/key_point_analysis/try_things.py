from debater_python_api.api.clients.key_point_analysis.KpAnalysisUtils import KpAnalysisUtils

if __name__ == '__main__':
    KpAnalysisUtils.init_logger()

    file = '/Users/yoavkantor/Documents/projects/keypoint-matching-kps-graphs-ui/static/data/default_results.json'
    KpAnalysisUtils.graph_data_to_hierarchical(file)