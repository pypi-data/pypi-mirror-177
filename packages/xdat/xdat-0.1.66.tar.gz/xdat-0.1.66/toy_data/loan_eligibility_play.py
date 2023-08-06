from sklearn.ensemble import RandomForestClassifier
from xdat.xincludes import *


def main():
    df = x_cached_call(xdata.read_csv, "/data/kaggle/loan_eligibility/Loan_Data.csv")
    xeda.x_inspect_cols(df)
    df['loan_id'] = df.loan_id.apply(lambda t: int(t[2:]))
    df['dependents'] = xpd.x_replace(df.dependents, replace_vals={'0': 0, '1': 1, '2': 2, '3+': 4})
    df['total_income'] = df.applicant_income + df.coapplicant_income
    df['applicant_ratio'] = df.loan_amount / df.applicant_income
    df['total_ratio'] = df.loan_amount / df.total_income
    # df['property_area_ord'] = xpd.x_replace(df.property_area, replace_vals={'Rural': 0, 'Semiurban': 0.5, 'Urban': 1.0})
    print('-----')
    xeda.x_inspect_cols(df)
    df_corr = xeda.x_corr_with_target(df, 'loan_status')
    cols_drop = set(df_corr[df_corr.abs_corr < 0.03].orig_col.values)
    cols_drop.add('loan_id')
    df.drop(columns=list(cols_drop), inplace=True)

    df, new_target = xeda.x_prep_df(df, 'loan_status')
    df.rename(columns={new_target: 'target'}, inplace=True)

    pipe = RandomForestClassifier(class_weight='balanced', min_samples_leaf=0.03, max_depth=5)
    df_test, all_folds = xproblem.train_cv(df, 'target', pipe, stratify_on='target')

    xplots.plot_roc_curve(all_folds[0].df_train.target, all_folds[0].df_train.prob_1, title='TRAIN')

    xplots.plot_confusion_matrix(df_test.target, df_test.pred, y_score=df_test.prob_1)

    df_eval = xproblem.eval_test(df_test, eval_per=['none'], metric_list=['AUC'])
    print(df_eval.to_string(index=False))

    print('Corr between model score & target:', np.corrcoef(df_test.prob_1, df_test.target)[0][1])

    xplots.plot_roc_curve(df_test.target, df_test.prob_1)
    xplots.plot_model_scores(df_test.target, df_test.prob_1)
    return


if __name__ == "__main__":
    main()
