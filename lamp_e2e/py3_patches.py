"""Minimal runtime patches so LAMP's Python 2 code runs under Python 3 (the repo itself is not edited)."""


def apply():
    import useful_functions as uf
    from Config import Config

    # PackingConfig.py does not define the GMM score thresholds MVGFit needs (only CafeWorldConfig
    # does: MVG_SCORE_THRESHOLD = 3). Use that value. SAMPLE_SCORE_THRESHOLD (MVGFit.belongs) is
    # defined nowhere in the repo; predict.py calibrates its own GMM threshold from training data.
    if not hasattr(Config, "MVG_SCORE_THRESHOLD"):
        Config.MVG_SCORE_THRESHOLD = 3
    if not hasattr(Config, "SAMPLE_SCORE_THRESHOLD"):
        Config.SAMPLE_SCORE_THRESHOLD = Config.MVG_SCORE_THRESHOLD

    def merge_dicts(dict1, dict2):
        # original: type(dict1.values()[0]); dict views are not indexable in py3
        if len(dict1) == 0:
            return dict(dict2)
        value_type = type(next(iter(dict1.values())))
        new_dict = dict1
        for k in dict2.keys():
            if k in new_dict:
                new_dict[k] = value_type(set(dict1[k]).union(set(dict2[k])))
            else:
                new_dict[k] = dict2[k]
        return new_dict

    uf.merge_dicts = merge_dicts
