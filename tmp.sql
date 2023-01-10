Select ngram,upos,avg(tfidf) as tfidf, convert(sum(tf),INT) as tf from (
SELECT tf.ngram, tf.upos,(0.5+0.5*(tf.tf/d.maxtf))*log(152000/df.df)*(-1*log(1-((dff.df)/(1+df.df)))) as tfidf, tf.tf as tf
FROM ngrams_upos_tf tf, documents d,
(
Select ngram, upos, count(*) as df from ngrams_upos_tf TF
 where document_id in
(select distinct document_id from metadata where  leto IN (2020) )
group by TF.ngram, TF.upos ) dff, ngrams_upos_df df
where
 tf.document_id=d.document_id and
df.ngram=tf.ngram AND df.upos=tf.upos and
dff.ngram=tf.ngram AND dff.upos=tf.upos
) X
group by ngram,upos
order by tfidf desc
limit 10;
