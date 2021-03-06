# the generator concept is adopted from paper
# https://arxiv.org/pdf/1710.11041.pdf
# we want to explore how output embedding parts differs woud affect performance

import vocab

import torch
import torch.nn as nn
import torch.nn.functional as F


# "traditional direct linear output fron embeddings"
class LinearGenerator( nn.Module ):

    def __init__( sself, hidden_size, vocab_size, bias = True ):
        super( LinearGenerator, self ).__init__()
        self.out = nn.Linear( hidden_size, data.NUM_SPECIAL_SYM + vocab_size, bias = bias )
        self.logsoftmax = nn.logsoftmax( dim = 1 )
    
    def forward( self, hidden ):
        self.logsoftmax( self.out( hidden ) )
        
    def num_output_class( self ):
        return self.out.weight.size()[ 0 ]

    def save_weight( self, path ):
        cpt  = dict()
        cpt[ "out" ] = self.state_dict()
        torch.save( cpt, path )
        print( "Successfully saved embedding" )

    def load_weight( self, path ):
        cpt = torch.load( path )
        self.load_state_dict( cpt[ "out" ] )
        print( "Successfully loaded embedding" )

class EmbeddingGenerator( nn.Module ):

    def __init__( self, hidden_size, embed_size ):
        super( EmbeddingGenerator, self ).__init__()
        self.hidden2embedding = nn.Linear( hidden_size, embed_size )
        self.special_out = nn.Linear( embed_size, vocab.NUM_SPECIAL_SYM, bias = False )
        self.logsoftmax = nn.LogSoftmax()

    def forward( self, hidden, embedding ):
        emb = self.hidden2embedding( hidden )
        word_scores = F.linear( emb, embedding.out.weight[ 1:, : ] )
        special_scores = self.special_out( emb )
        scores = torch.cat( ( special_scores, word_scores ), dim = 1 )
        return self.logsoftmax( scores )

class WrapperEmbeddingGenerator( nn.Module ):

    def __init__( self, embedding_generator, embed_out ):
        super( WrapperEmbeddingGenerator, self ).__init__()
        self.embedding_generator = embedding_generator
        self.embed_out = embed_out

    def forward( self, hidden ):
        return self.embedding_generator( hidden, self.embed_out )
    
    def num_output_class( self ):
        return self.embed_out.out.weight.data.size()[ 0 ] + vocab.NUM_SPECIAL_SYM - 1

    def save_weight( self, path ):
        cpt  = dict()
        cpt[ "out" ] = self.state_dict()
        torch.save( cpt, path )
        print( "Successfully saved embedding" )

    def load_weight( self, path ):
        cpt = torch.load( path )
        self.load_state_dict( cpt[ "out" ] )
        print( "Successfully loaded embedding" )

