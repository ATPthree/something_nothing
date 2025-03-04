import numpy as np
from numpy import linalg as la
from backend.recommender.data_loader import dl
from backend.app import scheduler, app


class Recommender:
    '''
    第一次使用前需要先调用fit，每次需要更新数据只需重新调用fit
    调用recommend返回推荐列表
    '''

    def __init__(self):
        self.data = None
        self.data_dir = None
        self.sim_mat = None
        scheduler.add_job(
            func=self.fit,  # 要执行的函数
            id='fit',  # 任务的ID
            trigger="interval",
            hours=24*7,
            replace_existing=True  # 如果存在同名任务，则替换
        )

    def __pearson_corr(self, vec_1: np.matrix, vec_2: np.matrix) -> float:
        mean_1 = np.mean(vec_1)
        mean_2 = np.mean(vec_2)
        num = float(((vec_1 - mean_1).T.dot(vec_2 - mean_2)).item())
        nom = la.norm(vec_1 - mean_1) * la.norm(vec_2 - mean_2)
        # return 0.5 + 0.5 * (num / nom) if nom != 0 else 0.0  # 归一化
        return (num / nom) if nom != 0 else 0.0

    def __pearson_corr_mat(self) -> np.ndarray:
        _, n = self.data.shape
        corr_mat = np.array(np.zeros((n, n)))
        for j in range(n):
            for i in range(j, n):
                corr_mat[i, j] = corr_mat[j, i] = self.__pearson_corr(self.data[:, j], self.data[:, i])
        return corr_mat

    def __food_score(self, user_id: str):
        # 如果用户没有点过菜，返回全0向量
        if user_id not in self.data_dir:
            return np.zeros(self.data.shape[1])
        user_feature = np.array(self.data_dir[user_id])
        rec_list = []
        for i, cnt in enumerate(tuple(user_feature)):
            if cnt > 0.0: continue  # 跳过用户已经吃过的菜品
            # score = (user_feature.dot(self.sim_mat[i].T)).item() / np.sum(self.sim_mat[i])
            score = ((user_feature - np.mean(user_feature)).dot(self.sim_mat[i].T)).item() / np.sum(self.sim_mat[i])
            rec_list.append((i, score))
        rec_list.sort(key=lambda x: x[1], reverse=True)
        return rec_list

    def __svd(self, rate: float):
        U, sigma, V_T = la.svd(self.data)
        sigmaSum = 0
        Sum = np.sum(sigma ** 2)
        n = len(sigma)
        for k in range(len(sigma)):
            sigmaSum += sigma[k] * sigma[k]
            if sigmaSum > rate * Sum:
                n = k + 1
                break
        if n == len(sigma):
            return
        sigma_k = np.mat(np.eye(n) * sigma[:n])
        self.data = sigma_k * U[:, :n].T * self.data


    def fit(self, rate: float = 0.9):
        '''rate为保留的奇异值比例,为0-1之间的小数，越小压缩越多'''
        self.data, self.data_dir = dl.load_data()
        self.__svd(rate)  # 奇异值分解,压缩数据
        self.sim_mat = self.__pearson_corr_mat()  # 计算皮尔逊相关系数矩阵

    def recommend(self, user_id, k: int = 3) -> list:
        '''k为推荐菜品数量'''
        rec_list = self.__food_score(user_id)
        # print(rec_list)
        return rec_list[:k]

rec = Recommender()
rec.fit()
